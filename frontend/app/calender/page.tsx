"use client";

import { useEffect, useState } from "react";

import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";

export default function CalendarPage() {
  const [events, setEvents] = useState<any[]>([]);

  // 처음 로딩할 때 저장된 데이터 불러오기
  useEffect(() => {
    const savedEvents =
      localStorage.getItem("events");

    if (savedEvents) {
      setEvents(JSON.parse(savedEvents));
    }
  }, []);

  // events 바뀔 때마다 저장
  useEffect(() => {
    localStorage.setItem(
      "events",
      JSON.stringify(events)
    );
  }, [events]);

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold mb-5">
        My Calendar
      </h1>

      <FullCalendar
        plugins={[
          dayGridPlugin,
          interactionPlugin,
        ]}
        initialView="dayGridMonth"
        events={events}
        dateClick={(info) => {
          const title = prompt("일정 제목");

          if (!title) return;

          setEvents([
            ...events,
            {
              title,
              date: info.dateStr,
            },
          ]);
        }}
      />
    </div>
  );
}