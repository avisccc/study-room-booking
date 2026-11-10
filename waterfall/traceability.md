# 瀑布組需求追溯表（Traceability Matrix）

> 本表依據 `waterfall/SRS.md` (v0.1) 建立，涵蓋 FR-01～FR-49 與 NFR-01～NFR-13，對應至 `waterfall/uml/` 下之類別圖（`class-diagram.md`）、狀態圖（`state-diagram.md`）與循序圖（`sequence-diagram.md`）。「程式(PR)」、「測試編號」將於建構與測試階段補齊；「對應的敏捷 story」將於跨組比較分析時由 C + D 填寫。

## 1. 功能需求追溯（FR-01 ～ FR-49）

| 需求編號 | 需求摘要 | 來源 | UML 對應 | 程式(PR) | 測試編號 | 對應的敏捷 story(比較用) |
|---|---|---|---|---|---|---|
| FR-01 | 身分選擇（輸入已建檔學號或選用共用館員身分，無密碼驗證） | SRC-01 | 類別圖：`Student.selectStudentIdentity()`、`LibrarianService.selectLibrarianIdentity()` | | | |
| FR-02 | 操作權限（學生資料隔離、僅預約者可修改取消、館員管理權限） | SRC-02 | 類別圖：`Student`、`LibrarianService`、`Booking`；循序圖 3.2 | | | |
| FR-03 | 房間與時段查詢（查看可用討論室、開放時間與指定時段狀況） | SRC-03 | 類別圖：`StudyRoom.searchAvailableRooms()`、`StudyRoom.isActive` | | | |
| FR-04 | 條件搜尋（依固定設備標籤、容納人數、日期時段篩選） | SRC-04 | 類別圖：`StudyRoom.searchAvailableRooms()`、`equipmentTags`、`capacity` | | | |
| FR-05 | 房間管理（新增、修改、停用討論室，保護既有有效預約與歷史） | SRC-05 | 類別圖：`StudyRoom.createRoom()`、`updateRoom()`、`deactivateRoom()` | | | |
| FR-06 | 開放時間管理（設定或修改各房開放時間，不得破壞既有有效預約） | SRC-06 | 類別圖：`RoomOpenSchedule`、`RoomOpenSchedule.updateOpenSchedule()` | | | |
| FR-07 | 館員查詢預約（依日期、房間或時段查看預約與當日狀態） | SRC-07 | 類別圖：`LibrarianService.queryBookings()`；循序圖 3.3 | | | |
| FR-08 | 建立預約（指定房間與起訖時間，單人直接成立、多人轉待確認、衝突可候補） | SRC-08 | 類別圖：`Booking.createBooking()`；狀態圖 2.1；循序圖 3.1 | | | |
| FR-09 | 我的紀錄（查詢本人作為預約者、受邀者、參與者或候補之紀錄） | SRC-09 | 類別圖：`Student.getMyRecords()`、`Booking`、`BookingInvitation`、`WaitlistEntry` | | | |
| FR-10 | 修改預約（僅預約者可修改已預約之房間或時間，不觸發遞補或重建候補） | SRC-10 | 類別圖：`Booking.modifyBooking()`；狀態圖 2.1 | | | |
| FR-11 | 取消預約（僅預約者可取消待確認或已預約，已預約取消觸發候補遞補） | SRC-11 | 類別圖：`Booking.cancelBooking()`；狀態圖 2.1；循序圖 3.2 | | | |
| FR-12 | 整點與時長（起訖須為整點，單次限 1、2、3 或 4 小時） | SRC-12 | 類別圖：`Booking.startTime`、`endTime`、`createBooking()`；循序圖 3.1 | | | |
| FR-13 | 每日時數（預約者每 Asia/Taipei 日期有效預約上限 8 小時，跨日拆計） | SRC-13 | 類別圖：`Booking.createBooking()`、`modifyBooking()`；循序圖 3.1 | | | |
| FR-14 | 有效筆數（每位預約者最多同時持有 10 筆有效預約） | SRC-14 | 類別圖：`Booking.createBooking()`；循序圖 3.1 | | | |
| FR-15 | 房間衝突（同房間有效預約左閉右開區間不可重疊） | SRC-15 | 類別圖：`Booking.createBooking()`；循序圖 3.1 | | | |
| FR-16 | 停權資格（停權中不可成立或遞補自身預約，可作為他人參與者） | SRC-16 | 類別圖：`SuspensionRecord`、`Booking.createBooking()`；循序圖 3.1 | | | |
| FR-17 | 時間與房間有效性（開始晚於現在、房間可用且整段位於開放時間內） | SRC-17 | 類別圖：`StudyRoom.isActive`、`RoomOpenSchedule`、`Booking.createBooking()`；循序圖 3.1 | | | |
| FR-18 | 修改與取消期限（已預約須距開始至少 3 小時；待確認須於開始前取消） | SRC-18 | 類別圖：`Booking.modifyBooking()`、`cancelBooking()`；狀態圖 2.1；循序圖 3.2 | | | |
| FR-19 | 額度與占用定義（僅未結束之已預約／已報到占房間與額度） | SRC-19 | 類別圖：`Booking`、`BookingStatus`；狀態圖 2.1；循序圖 3.1、3.2 | | | |
| FR-20 | 預約狀態（限待確認、已預約、已報到、已取消、已完成、未到場六種，候補另管） | SRC-20 | 類別圖：`BookingStatus`、`statusUpdatedAt`、`statusReason`；狀態圖 2.1 | | | |
| FR-21 | 發送邀請（以學號或 Email 邀請已建檔學生，不重複且不可邀自己） | SRC-21 | 類別圖：`Booking.createBooking()`、`BookingInvitation`；循序圖 3.1 | | | |
| FR-22 | 待確認階段（全員接受前為待確認、不占房與額度，到期未全員確認則取消） | SRC-22 | 類別圖：`BookingStatus.PENDING_CONFIRMATION`、`BookingInvitation`；狀態圖 2.1；循序圖 3.1 | | | |
| FR-23 | 接受與成立（全員接受後重驗規則，可預約則成立、僅房間衝突且同意候補則轉候補） | SRC-23 | 類別圖：`BookingInvitation.acceptInvitation()`；狀態圖 2.1；循序圖 3.1 | | | |
| FR-24 | 拒絕與取消（任一受邀者拒絕即整筆取消並結束未回覆邀請） | SRC-24 | 類別圖：`BookingInvitation.rejectInvitation()`；狀態圖 2.1；循序圖 3.1 | | | |
| FR-25 | 人數與容量（預約者加受邀者不得超過房間正整數容量） | SRC-25 | 類別圖：`StudyRoom.capacity`、`Booking.createBooking()`、`acceptInvitation()`；循序圖 3.1 | | | |
| FR-26 | 候補申請（與有效預約實際重疊時可申請候補，不占房間與額度） | SRC-26 | 類別圖：`WaitlistEntry.createWaitlist()`；狀態圖 2.2；循序圖 3.1 | | | |
| FR-27 | 多人候補（全員接受後遇房間衝突轉入候補，保留已接受參與者名單） | SRC-27 | 類別圖：`Booking.agreeToWaitlist`、`WaitlistEntry.participantIds`；狀態圖 2.1、2.2；循序圖 3.1 | | | |
| FR-28 | 名單與順序（每房共用候補名單、依加入時間排序，同人同房同時段不重複） | SRC-28 | 類別圖：`WaitlistEntry.roomId`、`createdAt`；循序圖 3.2 | | | |
| FR-29 | 候補退出（候補預約者於遞補前可主動退出並保留歷史） | SRC-29 | 類別圖：`WaitlistEntry.withdrawWaitlist()`；狀態圖 2.2 | | | |
| FR-30 | 取消觸發遞補（同房已預約整筆取消時，依序檢查完整時段空閒與規則進行遞補） | SRC-30 | 類別圖：`WaitlistEntry.processRoomWaitlistOnCancel()`；狀態圖 2.2；循序圖 3.2 | | | |
| FR-31 | 遞補失敗與結案（暫時不符跳過保留候補中；過期、退出、成功分別結案） | SRC-31 | 類別圖：`WaitlistEntry.status`、`lastSkipReason`、`expireIfPastStart()`；狀態圖 2.2；循序圖 3.2 | | | |
| FR-32 | 報到（開始起至 +10 分鐘含，館員確認預約者本人辦理一次報到） | SRC-32 | 類別圖：`Booking.checkIn()`、`checkedInAt`；狀態圖 2.1；循序圖 3.3 | | | |
| FR-33 | 未到場（逾開始 +10 分鐘未報到，於相關事件觸發時標為未到場並記點） | SRC-33 | 類別圖：`Booking.markNoShow()`、`BookingStatus.NO_SHOW`；狀態圖 2.1；循序圖 3.3 | | | |
| FR-34 | 完成使用（館員提前結束或到期由關聯事件觸發完成，並關閉設備） | SRC-34 | 類別圖：`Booking.completeUsage()`、`BookingStatus.COMPLETED`；狀態圖 2.1；循序圖 3.3 | | | |
| FR-35 | 我的點數（學生查看目前有效點數與停權狀態、結束時間） | SRC-35 | 類別圖：`Student.currentPoints`、`getMyPointsAndSuspension()` | | | |
| FR-36 | 館員違規處理（館員以整數手動加減點並記錄原因，減點採 FIFO） | SRC-36 | 類別圖：`LibrarianService.adjustStudentPoints()`、`PointAdjustmentLog`、`PenaltyPointItem` | | | |
| FR-37 | 未到場記點（每筆未到場僅對預約者加 1 點，記錄實際處理時間） | SRC-37 | 類別圖：`PenaltyPointItem`、`Booking.markNoShow()`；循序圖 3.3 | | | |
| FR-38 | 停權啟動（新增點數達 3 點以上且未停權時啟動 7 天停權） | SRC-38 | 類別圖：`SuspensionRecord`、`evaluateAndUpdateSuspension()`；循序圖 3.3 | | | |
| FR-39 | 停權更新／解除（停權中加點延長取較晚者；手動減至 <3 提前解禁） | SRC-39 | 類別圖：`SuspensionRecord.endAt`、`evaluateAndUpdateSuspension()`；循序圖 3.1、3.3 | | | |
| FR-40 | 點數自動恢復（每滿至少 7 天自動抵銷最早未抵銷之 1 點） | SRC-40 | 類別圖：`Student.lastAutoDecayAt`、`PenaltyPointItem.applyFifoDecayOrDeduct()`；循序圖 3.1、3.2 | | | |
| FR-41 | 事件通知（為指定業務事件建立對應收件人之通知紀錄） | SRC-41 | 類別圖：`NotificationRecord`；循序圖 3.1、3.2、3.3 | | | |
| FR-42 | 開始／結束提醒（館員查詢相關預約時產生 <=30min 開始與 <=10min 結束提醒寄予預約者） | SRC-42 | 類別圖：`LibrarianService.queryBookings()`、`NotificationRecord`；循序圖 3.3 | | | |
| FR-43 | 模擬寄送與重試（透過 Mock Mail Adapter 記錄待寄送／成功／失敗與館員重試） | SRC-43 | 類別圖：`NotificationRecord.sendViaMockAdapter()`、`LibrarianService.retryNotifications()`；循序圖 3.1～3.3 | | | |
| FR-44 | 通知去重（同一業務事件＋通知類型＋收件者不重複建立或寄送） | SRC-44 | 類別圖：`NotificationRecord.businessEventKey`、`sendViaMockAdapter()`；循序圖 3.1、3.3 | | | |
| FR-45 | 虛擬設備介面（獨立呈現各房間設備狀態、控制動作與結果） | SRC-45 | 類別圖：`VirtualDevice`；循序圖 3.3 | | | |
| FR-46 | 啟用控制（僅已報到預約之預約者於有效期間可要求啟用虛擬設備） | SRC-46 | 類別圖：`VirtualDevice.activateByRequester()`；狀態圖 2.1；循序圖 3.3 | | | |
| FR-47 | 結束關閉（預約完成或未到場時自動將虛擬設備設為關閉並記錄原因時間） | SRC-47 | 類別圖：`VirtualDevice.deactivateOnEndOrNoShow()`；狀態圖 2.1；循序圖 3.3 | | | |
| FR-48 | 關聯事件觸發（無背景排程，僅於業務關聯查詢或操作時更新該範圍到期狀態與提醒） | SRC-48 | 類別圖：各查詢與操作方法；循序圖 3.1、3.2、3.3 之關聯事件處理區塊 | | | |
| FR-49 | 館員稽核（保留館員成功之房間、時間、報到、點數、提前結束、通知重試操作紀錄） | SRC-49 | 類別圖：`LibrarianAuditLog`、`LibrarianService`；循序圖 3.3 | | | |

## 2. 非功能需求追溯（NFR-01 ～ NFR-13）

| 需求編號 | 需求摘要 | 來源 | UML 對應 | 程式(PR) | 測試編號 | 對應的敏捷 story(比較用) |
|---|---|---|---|---|---|---|
| NFR-01 | 資料存取控制（依學生身分限制私人資料存取，服務端拒絕未授權操作） | SRC-01, SRC-02, assumptions | 類別圖：`Student`、`Booking` 操作權限檢查；循序圖 3.2 | | | |
| NFR-02 | 重要業務資料持久保存（狀態與紀錄存於獨立 PostgreSQL 資料庫，歷史不隨停用刪除） | SRC-05, SRC-51, assumptions | 類別圖：所有持久化實體類別（對應 Prisma Schema） | | | |
| NFR-03 | 基本資料量驗證門檻（支援 100 學生、20 房間、5,000 筆預約紀錄之正確操作） | new | 類別圖：資料庫實體關聯與索引設計 | | | |
| NFR-04 | 跨裝置主要流程（支援手機與電腦瀏覽器完成主要操作） | SRC-50 | 循序圖 3.1～3.3 前端介面（Next.js + Tailwind CSS） | | | |
| NFR-05 | 瀏覽器與版面驗收基準（360px 與 1280px 視窗寬度無阻礙操作之水平溢出） | new | 循序圖 3.1～3.3 前端介面設計 | | | |
| NFR-06 | 操作一致性與失敗處理（核心業務無半筆交易，Mock Mail 失敗不回退核心交易） | SRC-43, SRC-52 | 類別圖：`NotificationRecord.sendViaMockAdapter()`；循序圖 3.1～3.3 | | | |
| NFR-07 | 穩定性驗證門檻（連續 30 分鐘每分鐘抽查至少 29 次成功） | new | 系統部署與資料庫連線架構 | | | |
| NFR-08 | 平行操作基本承載（10 人同時查詢或同房同時段競爭時最多一筆成功） | new, SRC-15, SRC-52 | 類別圖：`Booking.createBooking()`；循序圖 3.1 | | | |
| NFR-09 | 基本互動回應時間（查詢 P95 <= 5 秒，核心寫入 P95 <= 8 秒） | new | 類別圖与循序圖 3.1～3.3 僅針對關聯範圍更新（FR-48） | | | |
| NFR-10 | 可重建、審查與部署（提供 README，通過 TypeScript 與 Next.js 建置並部署至 Vercel） | new, assumptions | 整體專案結構（`waterfall/app/`） | | | |
| NFR-11 | 核心任務可完成性（未參與開發者 5 分鐘內完成查房預約與館員報到） | new, SRC-52 | 循序圖 3.1、3.3 使用者介面互動流程 | | | |
| NFR-12 | 管理操作可追查（保留館員各類成功管理操作之時間、類型與目標） | SRC-49, FR-49 | 類別圖：`LibrarianAuditLog`；循序圖 3.3 | | | |
| NFR-13 | 關聯更新與重複觸發一致性（重複查詢或操作不造成重複記點、狀態遷移或重複通知） | SRC-44, SRC-48, FR-48 | 類別圖：`NotificationRecord.businessEventKey`；循序圖 3.1～3.3 | | | |
