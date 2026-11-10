classDiagram
    direction TB

    class Student {
        +String id
        +String studentId "已建檔學號 (FR-01)"
        +String email "受邀查詢用 (FR-21)"
        +String name
        +Int currentPoints "目前有效點數 (FR-35)"
        +DateTime lastAutoDecayAt "前次自動恢復時間 (FR-40)"
        +selectStudentIdentity(studentId) Boolean "FR-01"
        +getMyRecords() List~Booking~ "FR-09"
        +getMyPointsAndSuspension() PointSummary "FR-35, FR-48"
    }

    class LibrarianService {
        <<Service>>
        +selectLibrarianIdentity() void "共用館員角色 (FR-01)"
        +queryBookings(date, roomId, timeRange) List~Booking~ "FR-07, FR-42, FR-48"
        +adjustStudentPoints(studentId, delta, reason) void "FR-36, FR-38, FR-39, FR-49"
        +retryNotifications(notificationIds) void "FR-43, FR-49"
    }

    class StudyRoom {
        +String id
        +String name "房間名稱 (FR-05)"
        +Int capacity "正整數容量 (FR-05, FR-25)"
        +String[] equipmentTags "固定設備標籤 (FR-04, FR-05)"
        +Boolean isActive "是否啟用 (FR-03, FR-05)"
        +createRoom(name, capacity, tags) StudyRoom "FR-05, FR-49"
        +updateRoom(id, name, capacity, tags) StudyRoom "檢查既有有效預約 (FR-05, FR-49)"
        +deactivateRoom(id) void "有未結束有效預約時拒絕 (FR-05, FR-49)"
        +searchAvailableRooms(date, start, end, minCap, tags) List~StudyRoom~ "FR-03, FR-04, FR-48"
    }

    class RoomOpenSchedule {
        +String id
        +String roomId
        +Int dayOfWeek "星期幾 或 特定日期 (FR-06)"
        +Int openHour "整點開放起時 (FR-06, FR-17)"
        +Int closeHour "整點開放迄時 (FR-06, FR-17)"
        +updateOpenSchedule(roomId, schedule) void "破壞既有有效預約時拒絕 (FR-06, FR-49)"
    }

    class Booking {
        +String id
        +String roomId
        +String requesterId "唯一預約者 (FR-08)"
        +DateTime startTime "整點開始時間 (FR-12, FR-17)"
        +DateTime endTime "整點結束時間 1~4hr (FR-12, FR-17)"
        +BookingStatus status "六種狀態 (FR-20)"
        +Boolean agreeToWaitlist "衝突時是否願意轉候補 (FR-21, FR-23, FR-27)"
        +DateTime checkedInAt "報到時間 (FR-32)"
        +DateTime statusUpdatedAt "狀態變動時間 (FR-20)"
        +String statusReason "變動/取消原因 (FR-20)"
        +createBooking(requesterId, roomId, start, end, invitees, agreeWaitlist) Booking "FR-08, FR-12~19, FR-21"
        +modifyBooking(requesterId, newRoomId, newStart, newEnd) Booking "距開始>=3hr (FR-10, FR-18)"
        +cancelBooking(requesterId) void "已預約須>=3hr; 觸發遞補 (FR-11, FR-18, FR-30)"
        +checkIn(librarian) void "開始~+10min內 (FR-32, FR-49)"
        +markNoShow() void "逾+10min未報到 (FR-33, FR-37, FR-47, FR-48)"
        +completeUsage(isEarlyByLibrarian) void "到期或提前結束 (FR-34, FR-47, FR-49)"
    }

    class BookingStatus {
        <<enumeration>>
        PENDING_CONFIRMATION "待確認 (FR-20, FR-22)"
        BOOKED "已預約 (FR-20)"
        CHECKED_IN "已報到 (FR-20, FR-32)"
        CANCELLED "已取消 (FR-20)"
        COMPLETED "已完成 (FR-20, FR-34)"
        NO_SHOW "未到場 (FR-20, FR-33)"
    }

    class BookingInvitation {
        +String id
        +String bookingId
        +String inviteeId "受邀學生 (FR-21)"
        +InvitationStatus status "PENDING | ACCEPTED | REJECTED | CLOSED (FR-22~24)"
        +DateTime respondedAt "回覆時間 (FR-23, FR-24)"
        +String reason "拒絕或結束原因 (FR-24)"
        +acceptInvitation(inviteeId) void "全員接受後重驗成立或轉候補 (FR-23, FR-25, FR-27)"
        +rejectInvitation(inviteeId, reason) void "一人拒絕整筆取消 (FR-24)"
    }

    class WaitlistEntry {
        +String id
        +String roomId "以討論室為單位 (FR-28)"
        +String requesterId "候補預約者 (FR-26)"
        +String[] participantIds "已接受之參與者名單 (FR-26, FR-27)"
        +DateTime startTime "完整開始時間 (FR-26)"
        +DateTime endTime "完整結束時間 (FR-26)"
        +WaitlistStatus status "WAITING | PROMOTED | WITHDRAWN | EXPIRED (FR-31)"
        +String lastSkipReason "暫時未通過原因 (FR-31)"
        +DateTime createdAt "依加入時間排序 (FR-28)"
        +createWaitlist(roomId, requesterId, participants, start, end) WaitlistEntry "FR-26, FR-27, FR-28"
        +withdrawWaitlist(requesterId) void "遞補前退出 (FR-29)"
        +processRoomWaitlistOnCancel(roomId) List~Booking~ "依序整段檢查遞補 (FR-30, FR-31)"
        +expireIfPastStart() void "到達開始時間標為已失效 (FR-31, FR-48)"
    }

    class PenaltyPointItem {
        +String id
        +String studentId
        +String sourceBookingId "來源未到場預約 (FR-37)"
        +DateTime occurredAt "實際處理伺服器時間 (FR-37)"
        +Boolean isOffset "是否已抵銷 (FR-40)"
        +DateTime offsetAt "抵銷時間 (FR-40)"
        +String offsetType "AUTO_DECAY | MANUAL_DEDUCT (FR-36, FR-40)"
        +applyFifoDecayOrDeduct(studentId) void "每7天自動消1點或手動FIFO減點 (FR-36, FR-40)"
    }

    class PointAdjustmentLog {
        +String id
        +String studentId
        +Int beforePoints "調整前點數 (FR-36)"
        +Int afterPoints "調整後點數 (FR-36)"
        +Int delta "差額 (FR-36)"
        +String reason "原因 (FR-36, FR-37)"
        +DateTime createdAt "異動時間 (FR-36)"
    }

    class SuspensionRecord {
        +String id
        +String studentId
        +DateTime startAt "停權起時 (FR-38)"
        +DateTime endAt "停權迄時 (+7天或延長取較晚) (FR-38, FR-39)"
        +String reason "啟動或更新原因 (FR-38, FR-39)"
        +Boolean isActive "是否生效中 (FR-38, FR-39)"
        +evaluateAndUpdateSuspension(studentId, isNewPointAdded, isManualDeduct) void "FR-16, FR-38, FR-39"
    }

    class NotificationRecord {
        +String id
        +String recipientId "收件人 (FR-41, FR-42)"
        +String businessEventKey "業務事件唯一識別 (FR-44)"
        +String notificationType "通知/提醒類型 (FR-41, FR-42)"
        +String status "PENDING | SENT | FAILED (FR-43)"
        +String content "通知內容 (FR-41)"
        +String failureReason "失敗原因 (FR-43)"
        +DateTime createdAt "建立時間 (FR-43)"
        +DateTime lastAttemptAt "嘗試寄送時間 (FR-43)"
        +sendViaMockAdapter() Boolean "去重並模擬寄送，失敗不回退交易 (FR-43, FR-44)"
    }

    class VirtualDevice {
        +String id
        +String roomId
        +Boolean isActivated "開啟/關閉狀態 (FR-45~47)"
        +String lastControlAction "最後控制動作 (FR-45)"
        +String triggerReason "觸發原因 (FR-46, FR-47)"
        +DateTime updatedAt "狀態時間 (FR-47)"
        +activateByRequester(bookingId, requesterId) void "僅已報到預約者可啟用 (FR-46)"
        +deactivateOnEndOrNoShow(bookingId, reason) void "完成或未到場自動關閉 (FR-34, FR-47)"
    }

    class LibrarianAuditLog {
        +String id
        +String actionType "房間/時間/報到/點數/提前結束/通知重試 (FR-49)"
        +String targetId "相關對象ID (FR-49)"
        +String details "異動摘要 (FR-49)"
        +DateTime createdAt "操作時間 (FR-49)"
    }

    Student "1" --> "0..*" Booking : 作為預約者建立 (FR-08)
    Student "1" --> "0..*" BookingInvitation : 收到邀請/參與 (FR-21)
    Student "1" --> "0..*" WaitlistEntry : 提出候補 (FR-26)
    Student "1" --> "0..*" PenaltyPointItem : 累計有效點數單位 (FR-37, FR-40)
    Student "1" --> "0..*" PointAdjustmentLog : 點數異動紀錄 (FR-36)
    Student "1" --> "0..*" SuspensionRecord : 停權紀錄 (FR-38, FR-39)
    Student "1" --> "0..*" NotificationRecord : 接收通知與提醒 (FR-41, FR-42)

    StudyRoom "1" --> "0..*" RoomOpenSchedule : 開放時間設定 (FR-06)
    StudyRoom "1" --> "0..*" Booking : 房間預約 (FR-08, FR-15)
    StudyRoom "1" --> "0..*" WaitlistEntry : 房間候補佇列 (FR-28)
    StudyRoom "1" --> "1..*" VirtualDevice : 綁定虛擬設備 (FR-45)

    Booking "1" --> "0..*" BookingInvitation : 包含受邀名單 (FR-21, FR-22)
    Booking --> BookingStatus : 狀態 (FR-20)
    LibrarianService ..> LibrarianAuditLog : 寫入成功操作稽核 (FR-49)