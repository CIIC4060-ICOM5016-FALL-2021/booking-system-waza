import React, {Component, useState, useEffect} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal} from "semantic-ui-react";


// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function Schedule(){
    const [dates, setDates] = useState([{
        'title': 'Selection',
        'allDay': false,
        'start': new Date(moment.now()),
        'end': new Date(moment.now())
    }]);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment)
    

    
    useEffect(() => {
	fetch("https://guarded-hamlet-30872.herokuapp.com/waza/userschedule/4")
	    .then(res => res.json())
	    .then(
		(result) => {
		    setDates(result)
		    setOpen(result)
		    console.log(result)
		},
	    )

    }, [])



    return <Container style={{ height: 800 }}><Calendar
        localizer={localizer}
        startAccessor="start"
        events={dates}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
    >

    </Calendar>
    </Container>


}
export default Schedule;
