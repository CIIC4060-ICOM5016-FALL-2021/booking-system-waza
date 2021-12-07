import React, {useState, useEffect} from 'react';
import {Calendar, momentLocalizer} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Grid, Form, Dimmer, Loader, Select} from "semantic-ui-react";
import DateTimeRangePicker from "@wojtekmaj/react-datetimerange-picker";

function RoomSchedule() {
    const logged_uid = localStorage.getItem('user_id');
    const [dates, setDates] = useState([]);
    const [openUnavailabilityDetail, setOpenUnavailabilityDetail] = useState(false);
    const [scheduleDetails, setScheduleDetails] = useState([]);
    const localizer = momentLocalizer(moment);
    const [deleteInProgress, setDeleteInProgress] = useState(false);
    const [openCreateUnavailability, setOpenCreateUnavailability] = useState(false);
    const [dateRangeValueUnavailability, onChangeDateRangeValueUnavailability] = useState([new Date(), moment(new Date()).add(30, 'm').toDate()]);
    const [roomsAvailable, setRoomsAvailable] = useState([]);
    const [newScheduleInformation, setNewScheduleInformation] = useState(new Map());
    const [disabledCreationForm, setDisabledCreationForm] = useState(true);

    const createUnavailability = (event, newValue) => {
        (async () => {
            let start_at = newScheduleInformation.get('start_at');
            let end_at = newScheduleInformation.get('end_at');
            let room_id = newScheduleInformation.get('room_id');
            let form_data = new FormData();
            form_data.append('start_at', start_at);
            form_data.append('end_at', end_at);
            form_data.append('room_id', room_id);

            const requestOptions = {
                method: 'POST',
                body: form_data
            };
            const response = await fetch(`https://guarded-hamlet-30872.herokuapp.com/waza/roomschedule/?user_id=${logged_uid}`, requestOptions);
            const data = await response.json();
            // console.log(data)
            getSchedule();
            setOpenCreateUnavailability(false)
        })();
    }

    const modifyUnavailabilityForm = (key, value) => {
        newScheduleInformation.set(key, value)
        console.log(newScheduleInformation);
    }

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
        onSelectSlot={(selected) => {
            let start_at = moment(selected['start']).format('MMM DD YYYY HH:mm:ss');
            let end_at = moment(selected['end']).format('MMM DD YYYY HH:mm:ss');
            onChangeDateRangeValueUnavailability([start_at, end_at]);
            modifyUnavailabilityForm('start_at', moment(selected['start']).format('YYYY-MM-DD HH:mm:ss'));
            modifyUnavailabilityForm('end_at', moment(selected['end']).format('YYYY-MM-DD HH:mm:ss'));

            setOpenCreateUnavailability(true);
        }}
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
        <Modal
            centered={false}
            open={openCreateUnavailability}
            onClose={() => setOpenCreateUnavailability(false)}
            onOpen={() => setOpenCreateUnavailability(true)}
        >
            <Modal.Header>Create a Unavailable Period</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    Please select an start and endtime for your unavailable period.
                </Modal.Description>
                <Grid columns={1} padded>
                    <Grid.Row>
                        <DateTimeRangePicker
                            onChange={onChangeDateRangeValueUnavailability}
                            value={dateRangeValueUnavailability}
                        />
                    </Grid.Row>
                    <Grid.Row>
                        <Button onClick={() => {
                            let start_at = moment(dateRangeValueUnavailability[0]).format('YYYY-MM-DD HH:mm:ss');
                            let end_at = moment(dateRangeValueUnavailability[1]).format('YYYY-MM-DD HH:mm:ss');
                            modifyUnavailabilityForm('start_at', start_at);
                            modifyUnavailabilityForm('end_at', end_at);

                            fetch(`https://guarded-hamlet-30872.herokuapp.com/waza/room_available/?start_at=${start_at}&end_at=${end_at}`)
                                .then(res => res.json())
                                .then(
                                    (result) => {
                                        let rooms = [];
                                        for (var r in result) {
                                            rooms.push({
                                                key: result[r]['id'],
                                                text: result[r]['name'],
                                                value: result[r]['id']
                                            });
                                        }
                                        setRoomsAvailable(rooms);
                                    },
                                )
                        }}>Find a Room</Button>
                    </Grid.Row>
                    <Grid.Row>
                        <Form>
                            <Form.Dropdown
                                label={'Room'}
                                required
                                disabled={roomsAvailable.length === 0}
                                control={Select}
                                options={roomsAvailable}
                                placeholder='Room'
                                search
                                searchInput={{id: 'form-select-control-room'}}
                                onChange={(event, newValue) => {
                                    modifyUnavailabilityForm('room_id', newValue.value);
                                    setDisabledCreationForm(false);
                                }}
                            />
                            <Button onClick={createUnavailability} disabled={disabledCreationForm}
                                    color={'green'}>Create Unavailability</Button>
                        </Form>
                    </Grid.Row>
                </Grid>


            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpenCreateUnavailability(false)}>X</Button>
            </Modal.Actions>
        </Modal>
        <Container fluid>
            <Button
                fluid
                onClick={() => {
                    setOpenCreateUnavailability(true)
                }}
            > Mark as unavailable</Button>
        </Container>
    </Container>


}

export default RoomSchedule;
