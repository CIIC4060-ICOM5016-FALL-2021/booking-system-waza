import React, {useState, useEffect} from 'react';
import {Calendar, momentLocalizer} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Grid, Form, Dimmer, Loader} from "semantic-ui-react";

function RoomSchedule() {
    const logged_uid = localStorage.getItem('user_id');
    const [dates, setDates] = useState([]);
    const [openUnavailabilityDetail, setOpenUnavailabilityDetail] = useState(false);
    const [scheduleDetails, setScheduleDetails] = useState([]);
    const localizer = momentLocalizer(moment);
    const [deleteInProgress, setDeleteInProgress] = useState(false);

    function getSchedule() {
        let events = [];
        fetch("https://guarded-hamlet-30872.herokuapp.com/waza/roomschedule/detail?user_id=10")
            .then(res => res.json())
            .then(
                (result) => {
                    for (var e in result) {
                        events.push({
                            'title': result[e]['room_name'],
                            'start': new Date(result[e]['start_at'] + '-0400 (AST)'),
                            'end': new Date(result[e]['end_at'] + '-0400 (AST)'),
                            'resources': {
                                'room_id': result[e]['room_id'],
                                'department_name': result[e]['department_name'],
                                'room_name': result[e]['room_name'],
                                'id': result[e]['id']
                            }
                        });
                    }
                    setDates(events);
                },
            );
    }

    function getScheduleDetails(event) {
        console.log(event)
        setScheduleDetails(event);
        setOpenUnavailabilityDetail(true);
    }

    const deleteUnavailability = () => {
        (async () => {
            setDeleteInProgress(true)
            const schedule_id = scheduleDetails['resources']['id'];
            console.log(schedule_id)
            const requestOptions = {
                method: 'DELETE',
            };
            const response = await fetch(`https://guarded-hamlet-30872.herokuapp.com/waza/roomschedule/${schedule_id}?user_id=${logged_uid}`, requestOptions);
            console.log(await response.json())
            setOpenUnavailabilityDetail(false);
            setDeleteInProgress(false)
            getSchedule();
        })();
    }

    useEffect(() => {
        getSchedule();
    }, [])

    return <Container style={{height: 800}}><Calendar
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
    </Calendar>
        <Modal
            centered={false}
            open={openUnavailabilityDetail}
            onClose={() => setOpenUnavailabilityDetail(false)}
            onOpen={() => setOpenUnavailabilityDetail(true)}
        >
            <Dimmer active={deleteInProgress} inverted>
                <Loader inverted>Deleting</Loader>
            </Dimmer>
            <Modal.Header>Room Unavailability Details</Modal.Header>
            <Modal.Content>
                <Grid columns={2} padded>
                    <Grid.Row>
                        <Grid.Column>
                            <Form>
                                <Card fluid>
                                    <Card.Content header={scheduleDetails['title']}/>
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
                                <Button negative onClick={deleteUnavailability}>Delete Schedule</Button>
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

export default RoomSchedule;
