# 瀑布組 UML 循序圖（Sequence Diagram）

> 依據 `waterfall/SRS.md` 階段二建模規範，系統循序圖涵蓋「預約與多人邀請／候補」、「取消預約與自動遞補」以及「館員報到、未到場記點與虛擬設備控制」三大業務流程。所有流程皆嚴格落實無背景排程（FR-48）之被動關聯觸發機制與 Mock Mail 去重規則（FR-44）。

---

## 1. 預約與多人邀請／候補循序圖

* **對應需求**：FR-08、FR-12～19、FR-21～28、FR-41、FR-43、FR-44、FR-48
* **說明**：涵蓋單人直接預約、多人邀請待確認轉成立，以及時段衝突轉入候補名單的完整判定路徑。

```mermaid
sequenceDiagram
    autonumber
    actor Req as 預約者 (學生)
    actor Inv as 受邀者 (學生)
    participant UI as 學生端介面 (Next.js)
    participant Svc as 預約與關聯事件服務
    participant DB as 資料庫 (PostgreSQL / Prisma)
    participant Mail as Mock Mail Adapter

    Req->>UI: 查詢房間時段 / 送出預約申請 (含受邀學號、同意候補意向)
    UI->>Svc: requestBooking(requesterId, roomId, start, end, invitees, agreeWaitlist)
    
    Note over Svc,DB: 依 FR-48：處理該房間時段相關到期狀態與預約者個人恢復
    Svc->>DB: 更新該房間逾期未報到預約為「未到場」與到期「已完成」[FR-33, FR-34, FR-48]
    Svc->>DB: 補算預約者到期點數恢復 (每滿7天消1點) 與解除到期停權 [FR-39, FR-40, FR-48]
    
    Svc->>DB: 驗證規則：整點1~4hr、每日<=8hr、有效<=10筆、未停權、開放時間與容量 [FR-12~17, FR-25]
    
    alt 基礎規則或資格檢查不符
        Svc-->>UI: 拒絕申請並回傳錯誤訊息 (如：停權中、超過每日上限)
    else 單人預約 (無受邀者)
        Svc->>DB: 檢查同房間左閉右開時段是否衝突 [FR-15, FR-19]
        alt 無時段衝突
            Svc->>DB: 建立 Booking (status = 已預約) [FR-08]
            Svc->>Mail: 建立並嘗試模擬寄送「預約成立通知」給預約者 [FR-41, FR-43, FR-44]
            Svc-->>UI: 回傳預約成功 (已預約)
        else 時段衝突 且 勾選同意候補
            Svc->>DB: 建立 WaitlistEntry (status = 候補中，記錄加入時間) [FR-26, FR-28]
            Svc-->>UI: 回傳已加入房間候補名單
        end
    else 多人預約 (有受邀者)
        Svc->>DB: 建立 Booking (status = 待確認) 與 BookingInvitation 清單 [FR-21, FR-22]
        Svc->>Mail: 建立並嘗試寄送「邀請通知」給所有受邀者 [FR-21, FR-41, FR-43]
        Svc-->>UI: 回傳已建立待確認預約 (不占用房間與額度) [FR-19, FR-22]
        
        Inv->>UI: 受邀者查看邀請並進行回覆 [FR-23, FR-24]
        UI->>Svc: respondInvitation(invitationId, inviteeId, action)
        Svc->>DB: 檢查該待確認是否已過開始時間 (逾期則取消並結束邀請) [FR-22, FR-48]
        alt 受邀者點擊拒絕
            Svc->>DB: 更新 Booking 為「已取消」，結束其餘未回覆邀請 [FR-24]
            Svc->>Mail: 寄送取消通知給預約者與全體受邀者 [FR-24, FR-41]
        else 受邀者點擊接受 (成為最後一位確認者，全員同意)
            Svc->>DB: 依最新房間狀態、容量、預約者資格與 F03 規則重驗 [FR-23, FR-25]
            alt 規則重驗通過 且 房間無衝突
                Svc->>DB: 更新 Booking 為「已預約」[FR-23]
                Svc->>Mail: 去重寄送單次「預約成立通知」給全體參與名單 [FR-41, FR-44]
            else 僅房間衝突 且 預約者發起時同意候補
                Svc->>DB: Booking 結案為「已取消(轉候補)」，建立含名單之 WaitlistEntry (候補中) [FR-23, FR-27]
                Svc->>Mail: 通知預約者與已確認參與者「已轉入候補」[FR-27, FR-41]
            else 重驗失敗 或 未同意候補
                Svc->>DB: 更新 Booking 為「已取消」並記錄原因 [FR-23]
                Svc->>Mail: 通知全體成員成立失敗原因 [FR-23, FR-41]
            end
        end
    end
```

---

## 2. 取消預約與候補自動遞補循序圖

* **對應需求**：FR-02、FR-11、FR-18、FR-19、FR-30、FR-31、FR-41、FR-43、FR-44、FR-48
* **說明**：展現學生取消預約時的 3 小時期限檢核，以及已預約取消時觸發同房間多筆候補之循序無裁切遞補流程。

```mermaid
sequenceDiagram
    autonumber
    actor Req as 預約者 (學生)
    participant UI as 學生端介面 (Next.js)
    participant Svc as 預約與候補遞補服務
    participant DB as 資料庫 (PostgreSQL / Prisma)
    participant Mail as Mock Mail Adapter

    Req->>UI: 點擊「取消預約」
    UI->>Svc: cancelBooking(bookingId, requesterId)
    Svc->>DB: 查詢預約資料、身分與當下伺服器時間 [FR-02, FR-11]

    alt 非預約者本人 或 (已預約 且 距離開始時間 < 3 小時) 或 預約已開始
        Svc-->>UI: 拒絕取消操作並回傳原因 [FR-02, FR-11, FR-18]
    else 狀態為「待確認」於開始前取消
        Svc->>DB: 更新 Booking 為「已取消」，結束所有未回覆邀請 (不觸發遞補) [FR-11]
        Svc->>Mail: 寄送取消通知給所有受邀者與預約者 [FR-11, FR-41]
        Svc-->>UI: 回傳待確認已取消
    else 狀態為「已預約」且 距離原開始時間 >= 3 小時
        Svc->>DB: 更新 Booking 為「已取消」(釋出房間時段與預約者額度) [FR-11, FR-19]
        Svc->>Mail: 寄送預約取消通知給預約者及已接受之參與者 [FR-41]
        
        Note over Svc,DB: 依 FR-30, FR-31：同房間依加入順序 (createdAt) 逐筆檢查候補名單
        Svc->>DB: 取得該 roomId 所有 status = 候補中 之申請清單 [FR-28, FR-30]
        loop 依序整段檢查每一筆候補申請
            alt 候補開始時間已過
                Svc->>DB: 更新 WaitlistEntry 為「已失效」[FR-31]
                Svc->>Mail: 通知候補成員「候補已失效」[FR-41]
            else 候補尚未過期
                Svc->>DB: 補算候補預約者點數恢復與停權資格 [FR-40, FR-48]
                Svc->>DB: 檢核完整時段是否全段空閒 (不裁切)，且全體成員符合 F03/F04 規則 [FR-30]
                alt 時段空閒 且 規則重驗通過
                    Svc->>DB: 更新 WaitlistEntry 為「已遞補」，建立新 Booking (已預約，保留參與者) [FR-30, FR-31]
                    Svc->>Mail: 寄送「候補遞補成功通知」給候補全體成員 [FR-30, FR-41]
                else 時段仍衝突 或 預約者額度/資格不符
                    Svc->>DB: 維持「候補中」並記錄本輪跳過原因，不中斷迴圈繼續檢查下一筆 [FR-31]
                end
            end
        end
        Svc-->>UI: 回傳取消成功
    end
```

---

## 3. 館員報到、未到場記點與虛擬設備控制循序圖

* **對應需求**：FR-07、FR-32～40、FR-42、FR-45～49
* **說明**：展示館員查詢時被動觸發未到場判定（逾開始 10 分鐘記 1 點）、開始/結束通知提醒、預約者啟用虛擬設備，以及提前結束或到期之設備關閉與館員操作稽核。

```mermaid
sequenceDiagram
    autonumber
    actor Lib as 館員
    actor Req as 預約者 (學生)
    participant UI as 系統介面 (館員端/學生端)
    participant Svc as 報到、違規與設備服務
    participant Dev as 獨立虛擬設備介面
    participant DB as 資料庫 (PostgreSQL / Prisma)
    participant Mail as Mock Mail Adapter

    Lib->>UI: 依日期/房間查詢當日預約清單 [FR-07]
    UI->>Svc: queryRoomBookings(roomId, date, filterType)
    
    Note over Svc,DB: 依 FR-48 / 5.5 節：於查詢範圍內檢查逾期未到場與提醒
    Svc->>DB: 檢索查詢範圍內「已預約」且 當下時間 > 開始時間 + 10 分鐘 之紀錄 [FR-33, FR-48]
    loop 逐筆處理逾期未到場預約
        Svc->>DB: 標記 Booking 為「未到場」，對預約者新增 1 筆 PenaltyPointItem (+1pt) [FR-33, FR-37]
        Svc->>DB: 若累積有效點數達 3 點以上：未停權者啟動 7 天停權；已停權者延長期限 [FR-38, FR-39]
        Svc->>Dev: 同步關閉對應房間虛擬設備並記錄原因 [FR-47]
        Svc->>Mail: 寄送未到場記點與停權變動通知給預約者 [FR-41, FR-43]
    end
    Svc->>DB: 依查詢時段產生 <=30min 開始提醒 或 <=10min 結束提醒 (去重僅寄預約者) [FR-42, FR-44]
    Svc-->>UI: 回傳最新預約清單

    Lib->>UI: 確認預約者本人到場，辦理報到 [FR-32]
    UI->>Svc: checkInBooking(bookingId)
    alt 當下時間落在 [開始時間, 開始時間 + 10 分鐘] 且狀態為「已預約」
        Svc->>DB: 更新 Booking 為「已報到」並記錄報到時間 [FR-32]
        Svc->>DB: 寫入 LibrarianAuditLog (記錄報到操作與時間) [FR-49]
        Svc-->>UI: 報到成功
        
        Req->>UI: 預約者於使用期間請求啟用設備 [FR-46]
        UI->>Svc: activateDevice(bookingId, requesterId)
        Svc->>Dev: 驗證為已報到預約者本人，發出啟用請求並更新狀態 [FR-45, FR-46]
        Dev-->>UI: 虛擬設備介面顯示門禁/電源已開啟
        
        Lib->>UI: 館員手動點擊「提前結束」(或到達結束時間由關聯操作處理) [FR-34, FR-48]
        UI->>Svc: completeBooking(bookingId, isEarlyByLibrarian)
        Svc->>DB: 更新 Booking 為「已完成」；若為館員操作則寫入 LibrarianAuditLog [FR-34, FR-49]
        Svc->>Dev: 自動切換房間虛擬設備為「關閉/停用」[FR-34, FR-47]
        Dev-->>UI: 虛擬設備介面顯示已關閉
    else 未達開始時間 或 已逾 10 分鐘寬限 或 狀態不符
        Svc-->>UI: 拒絕報到並顯示原因 [FR-32]
    end
```