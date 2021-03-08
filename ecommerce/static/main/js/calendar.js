$('#calendar').fullCalendar({
    header: {
        left: 'prev,next today',
        center: 'title',
        right: 'month,agendaWeek,agendaDay,listWeek'
    },
    defaultDate: '2018-11-16',
    navLinks: true,
    eventLimit: true,
    events: [{
            title: 'Front-End Conference',
            start: '2018-11-16',
            end: '2018-11-18'
        },
        {
            title: 'Hair stylist with Mike',
            start: '2018-11-20',
            allDay: true
        },
        {
            title: 'Car mechanic',
            start: '2018-11-14T09:00:00',
            end: '2018-11-14T11:00:00'
        },
        {
            title: 'Dinner with Mike',
            start: '2018-11-21T19:00:00',
            end: '2018-11-21T22:00:00'
        },
        {
            title: 'Chillout',
            start: '2018-11-15',
            allDay: true
        },
        {
            title: 'Vacation',
            start: '2018-11-23',
            end: '2018-11-29'
        },
    ]
});

JS

$('#calendar').fullCalendar({
  header: {
    left: 'prev,next today',
    center: 'addEventButton',
    right: 'month,agendaWeek,agendaDay,listWeek'
  },
  defaultDate: '2018-11-16',
  navLinks: true,
  editable: true,
  eventLimit: true,
  events: [{
      title: 'Simple static event',
      start: '2018-11-16',
      description: 'Super cool event'
    },

  ],
  customButtons: {
    addEventButton: {
      text: 'Add new event',
      click: function () {
        var dateStr = prompt('Enter date in YYYY-MM-DD format');
        var date = moment(dateStr);

        if (date.isValid()) {
          $('#calendar').fullCalendar('renderEvent', {
            title: 'Dynamic event',
            start: date,
            allDay: true
          });
        } else {
          alert('Invalid Date');
        }

      }
    }
  },
  dayClick: function (date, jsEvent, view) {
    var date = moment(date);

    if (date.isValid()) {
      $('#calendar').fullCalendar('renderEvent', {
        title: 'Dynamic event from date click',
        start: date,
        allDay: true
      });
    } else {
      alert('Invalid');
    }
  },
});