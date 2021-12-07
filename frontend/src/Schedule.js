import React, {Component, useState, useEffect} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Grid, Form} from "semantic-ui-react";


// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function Schedule(){
    const logged_uid = localStorage.getItem('user_id');
    const [dates, setDates] = useState([{
        'title': 'Selectio',
        'allDay': false,
        'start': new Date(moment.now()),
        'end': new Date(moment.now())
    }]);
    const [open, setOpen] = useState(false);

    const [openUnavailabilityDetail, setOpenUnavailabilityDetail] = useState(false);
    const [scheduleDetails, setScheduleDetails] = useState([]);
    const localizer = momentLocalizer(moment);

    function getSchedule(){
	let events = [];
	fetch(`https://guarded-hamlet-30872.herokuapp.com/waza/userschedule?user_id=${logged_uid}`)
                    .then(res => res.json())
                    .then(
                        (result) => {
                            for (var e in result) {
                                events.push({
                                    'title': '- Not Available -',
                                    'start': new Date(result[e]['start_at'] + '-0400 (AST)'),
                                    'end': new Date(result[e]['end_at'] + '-0400 (AST)'),
                                    'resources': {'type': 'unavailable', 'schedule_id': result[e]['id']}
                                });
                            }
                            setDates(events);
			    for (var event in events) {
				console.log(e);
			    }
                        },
                    );
    }

    function getScheduleDetails(event) {
        console.log(event);
        setScheduleDetails(event);
        setOpenUnavailabilityDetail(true);
    }

    useEffect(() => {
	getSchedule();
    }, [])


    return <Container style={{ height: 800 }}><Calendar
        selectable
        localizer={localizer}
        startAccessor="start"
        events={dates}
        endAccessor="end"
    views={["month", "week", "day"]}
    defaultDate={new Date()}
    onSelectEvent={(selected) => {
        getScheduleDetails(selected);
    }}
	>
	//getSchedule();
    </Calendar>
	 <Modal
            centered={false}
            open={openUnavailabilityDetail}
            onClose={() => setOpenUnavailabilityDetail(false)}
            onOpen={() => setOpenUnavailabilityDetail(true)}
        >
            <Modal.Header>Unavailability Details</Modal.Header>
            <Modal.Content>
                <Grid columns={2} padded>
                    <Grid.Row>
                        <Grid.Column>
                            <Form>
                                <Card fluid>
                                    <Card.Content header={'Unavailable Period'}/>
                                    <Card.Content>
                                        <p>
                                            <b>Start
                                                At:</b> {(moment(scheduleDetails['start']).format('dddd, MMMM Do YYYY, h:mm a'))}
                                            <br/>
                                            <b>End
                                                At:</b> {(moment(scheduleDetails['end']).format('dddd, MMMM Do YYYY, h:mm a'))}
                                        </p>
                                    </Card.Content>
                                </Card>
                            </Form>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>


            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpenUnavailabilityDetail(false)}>X</Button>
            </Modal.Actions>
        </Modal>
	    </Container>


}
export default Schedule;
