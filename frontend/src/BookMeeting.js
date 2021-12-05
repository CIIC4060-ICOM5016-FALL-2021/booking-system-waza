import React, {useEffect, useState} from 'react';
import {Calendar, momentLocalizer} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Grid, Modal, Select} from "semantic-ui-react";
import DateTimeRangePicker from '@wojtekmaj/react-datetimerange-picker'

// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function BookMeeting() {
    const [dates, setDates] = useState([]);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment);
    const [value, onChange] = useState([new Date(), new Date()]);
    const [roomsAvailable, setRoomsAvailable] = useState([]);
    const [usersAvailable, setUsersAvailable] = useState([])
    const [newMeetingInformation, setNewMeetingInformation] = useState(new Map())

    const modifyMeetingForm = (key, value) => {
        newMeetingInformation.set(key, value)
        console.log(newMeetingInformation);
    }

    const handleMeetingCreation = (event, newValue) => {
        setOpen(true);
        (async () => {
            var form_data = new FormData();
            for (let [key, value] of newMeetingInformation) {
                form_data.append(key, value);
            }

            const requestOptions = {
                method: 'POST',
                body: form_data
            };
            const response = await fetch('http://127.0.0.1:5000/waza/meeting_with_invitees/', requestOptions);
            const data = await response.json();
            getMeetings();
            setOpen(false)
        })();
    }

    function getMeetings() {
        fetch("http://127.0.0.1:5000/waza/meeting/?user_id=1")
            .then(res => res.json())
            .then(
                (result) => {
                    let events = [];
                    for (var e in result) {
                        events.push({
                            'title': result[e]['room_name'],
                            'start': new Date(result[e]['start_at']+'-0400 (AST)'),
                            'end': new Date(result[e]['end_at']+'-0400 (AST)')
                        });
                    }
                    setDates(events);
                },
            );
    }

    useEffect(() => {
        // initial value
        modifyMeetingForm('created_by', 1)
        getMeetings();
    }, [])

    return <Container style={{height: 800}}>
        <Calendar
            selectable
            localizer={localizer}
            startAccessor="start"
            events={dates}
            endAccessor="end"
            views={["month", "week", "day"]}
            defaultDate={new Date()}
            onSelectSlot={(selected) => {
                console.log(selected)
            }}
            // onSelecting={(selected) => {
            //     setDates([{
            //         'title': 'Selection',
            //         'allDay': false,
            //         'start': new Date(selected.start),
            //         'end': new Date(selected.end)
            //     }])
            //     // let d = dates
            //     // d.push({
            //     //     'title': 'Selection',
            //     //     'allDay': false,
            //     //     'start': new Date(selected.start),
            //     //     'end': new Date(selected.end)
            //     // })
            //     // console.log(d)
            //     // setDates(d)
            // }}
        >

        </Calendar>
        <Modal
            centered={false}
            open={open}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}
        >
            <Modal.Header>Create a Meeting</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    Please select an start and endtime for your meeting.
                </Modal.Description>
                <Grid columns={1} padded>
                    <Grid.Row>
                        <DateTimeRangePicker
                            onChange={onChange}
                            value={value}
                        />
                    </Grid.Row>
                    <Grid.Row>
                        <Button onClick={() => {
                            let start_at = moment(value[0]).format('YYYY-MM-DD HH:mm:ss');
                            let end_at = moment(value[1]).format('YYYY-MM-DD HH:mm:ss');
                            modifyMeetingForm('start_at', start_at);
                            modifyMeetingForm('end_at', end_at)

                            fetch(`http://127.0.0.1:5000/waza/room_available/?start_at=${start_at}&end_at=${end_at}`)
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
                            //get available users
                            fetch(`http://127.0.0.1:5000/waza/user`)
                                .then(res => res.json())
                                .then(
                                    (result) => {
                                        let users = [];
                                        for (var r in result) {
                                            users.push({
                                                key: result[r]['id'],
                                                text: result[r]['email'],
                                                value: result[r]['id']
                                            });
                                        }
                                        setUsersAvailable(users);
                                    },
                                )
                            // setOpen(false)
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
                                onChange={(event, newValue) => modifyMeetingForm('room_id', newValue.value)}
                            />
                            <Form.Dropdown
                                label={'Invitees'}
                                required
                                disabled={roomsAvailable.length === 0}
                                placeholder='Invitees'
                                fluid
                                multiple
                                search
                                selection
                                options={usersAvailable}
                                onChange={(event, newValue) => modifyMeetingForm('users', ("[" + (newValue.value).toString() + "]"))}
                            />
                            <Button onClick={handleMeetingCreation} disabled={roomsAvailable.length === 0} color={'green'}>Create
                                Meeting</Button>
                        </Form>
                    </Grid.Row>
                </Grid>


            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpen(false)}>X</Button>
            </Modal.Actions>
        </Modal>
        <Container fluid>
            <Button
                fluid
                onClick={() => {
                    setOpen(true)
                }}
            > Book Meeting </Button>
            <Button
                fluid
                onClick={() => {
                    setOpen(true)
                }}
            > Mark as unavailable</Button>
        </Container>
    </Container>


}

export default BookMeeting;
