import React, {useEffect, useState} from 'react';
import {Calendar, momentLocalizer} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {
    Button,
    Card,
    Container,
    Form,
    Grid,
    Modal,
    Select,
    Feed,
    Divider,
    Confirm,
    Dimmer,
    Loader
} from "semantic-ui-react";
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
    const [openCreateUnavailability, setOpenCreateUnavailability] = useState(false);
    const [openMeetingDetail, setOpenMeetingDetail] = useState(false);
    const [openUnavailabilityDetail, setOpenUnavailabilityDetail] = useState(false);
    const [updateInProgress, setUpdateInProgress] = useState(false);
    const [deleteInProgress, setDeleteInProgress] = useState(false);
    const [deleteInProgressUnavailability, setDeleteInProgressUnavailability] = useState(false);
    const localizer = momentLocalizer(moment);
    const [dateRangeValue, onChangeDateRangeValue] = useState([new Date(), new Date()]);
    const [dateRangeValueUnavailability, onChangeDateRangeValueUnavailability] = useState([new Date(), moment(new Date()).add(30, 'm').toDate()]);
    const [roomsAvailable, setRoomsAvailable] = useState([]);
    const [usersAvailable, setUsersAvailable] = useState([]);
    const [newMeetingInformation, setNewMeetingInformation] = useState(new Map());
    const [meetingDetails, setMeetingDetails] = useState([]);
    const [meetingInvitees, setMeetingInvitees] = useState([]);
    const [scheduleDetails, setScheduleDetails] = useState([]);

    const modifyMeetingForm = (key, value) => {
        newMeetingInformation.set(key, value)
        console.log(newMeetingInformation);
    }

    const modifyMeetingDetails = (key, value) => {
        let tmp = meetingDetails;
        tmp[key] = value;
        setMeetingDetails(tmp);
        console.log(meetingDetails);
    }

    const createMeeting = (event, newValue) => {
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
            console.log(data)
            getMeetings();
            setOpen(false)
        })();
    }

    const createUnavailability = (event, newValue) => {
        (async () => {
            let start_at = moment(dateRangeValueUnavailability[0]).format('YYYY-MM-DD HH:mm:ss');
            let end_at = moment(dateRangeValueUnavailability[1]).format('YYYY-MM-DD HH:mm:ss');
            let form_data = new FormData();

            form_data.append('user_id', 3);
            form_data.append('start_at', start_at);
            form_data.append('end_at', end_at);

            const requestOptions = {
                method: 'POST',
                body: form_data
            };
            const response = await fetch('http://127.0.0.1:5000/waza/userschedule', requestOptions);
            const data = await response.json();
            console.log(data)
            getMeetings();
            setOpenCreateUnavailability(false)
        })();
    }

    const deleteMeeting = (event, newValue) => {
        (async () => {
            setDeleteInProgress(true)
            const requestOptions = {
                method: 'DELETE',
            };

            for (var i in meetingInvitees) {
                const response = await fetch(`http://127.0.0.1:5000/waza/invitee/${meetingInvitees[i]['invitee_id']}?user_id=3`, requestOptions);
                console.log(await response.json())
            }

            const response = await fetch(`http://127.0.0.1:5000/waza/meeting/${meetingDetails['meeting_id']}?user_id=3`, requestOptions);
            const data = await response.json();
            console.log(data)
            setOpenMeetingDetail(false);
            setDeleteInProgress(false)
            getMeetings();
        })();
    }

    const deleteInvitee = (invitee_id) => {
        (async () => {
            setDeleteInProgress(true)
            const requestOptions = {
                method: 'DELETE',
            };
            const response = await fetch(`http://127.0.0.1:5000/waza/invitee/${invitee_id}?user_id=3`, requestOptions);
            console.log(await response.json())
            setOpenMeetingDetail(false);
            setDeleteInProgress(false)
            getMeetings();
        })();
    }

    const deleteUnavailability = (event, newValue) => {
        (async () => {
            setDeleteInProgressUnavailability(true)
            const requestOptions = {
                method: 'DELETE',
            };

            const response = await fetch(`http://127.0.0.1:5000/waza/userschedule/${(scheduleDetails['resources']['schedule_id'])}`, requestOptions);
            const data = await response.json();
            console.log(data);
            setOpenUnavailabilityDetail(false);
            setDeleteInProgressUnavailability(false)
            getMeetings();
        })();
    }

    function getMeetings() {
        let events = [];

        fetch("http://127.0.0.1:5000/waza/meeting/?user_id=1")
            .then(res => res.json())
            .then(
                (result) => {
                    for (var e in result) {
                        events.push({
                            'title': result[e]['room_name'],
                            'start': new Date(result[e]['start_at'] + '-0400 (AST)'),
                            'end': new Date(result[e]['end_at'] + '-0400 (AST)'),
                            'resources': {'meeting_id': result[e]['id'], 'room_id': result[e]['room_id'], 'type': 'meeting'}
                        });
                    }
                },
            ).then(
            (result) => {
                fetch("http://127.0.0.1:5000/waza/userschedule?user_id=3")
                    .then(res => res.json())
                    .then(
                        (result) => {
                            for (var e in result) {
                                events.push({
                                    'title': '- Set as Not Available -',
                                    'start': new Date(result[e]['start_at'] + '-0400 (AST)'),
                                    'end': new Date(result[e]['end_at'] + '-0400 (AST)'),
                                    'resources': {'type': 'unavailable', 'schedule_id': result[e]['id']}
                                });
                            }
                            setDates(events);
                        },
                    );
            },
        )


        // setDates(events);
    }

    function getMeetingDetails(meeting_id, room_id) {
        fetch(`http://127.0.0.1:5000/waza/meeting_with_invitees/${meeting_id}`)
            .then(res => res.json())
            .then(
                (result) => {
                    let mDetail = [];
                    for (var e in result) {
                        mDetail.push({
                            "end_at": result[e]['end_at'],
                            "meeting_creator_email": result[e]['meeting_creator_email'],
                            "meeting_creator_first_name": result[e]['meeting_creator_first_name'],
                            "meeting_creator_last_name": result[e]['meeting_creator_last_name'],
                            "meeting_creator_id": result[e]['meeting_creator_id'],
                            "meeting_creator_phone": result[e]['meeting_creator_phone'],
                            "invitee_user_email": result[e]['invitee_user_email'],
                            "invitee_user_first_name": result[e]['invitee_user_first_name'],
                            "invitee_user_id": result[e]['invitee_user_id'],
                            "invitee_user_last_name": result[e]['invitee_user_last_name'],
                            "invitee_user_phone": result[e]['invitee_user_phone'],
                            "meeting_id": result[e]['meeting_id'],
                            "start_at": result[e]['start_at'],
                            "name": result[e]['name'],
                            "description": result[e]['description'],
                            "invitee_id": result[e]['invitee_id'],
                            "room_id": room_id
                        });
                    }
                    setMeetingDetails(mDetail.length > 0 ? mDetail[0] : null);
                    setMeetingInvitees(mDetail);
                    setOpenMeetingDetail(true);
                },
            );
    }

    function getScheduleDetails(event) {
        console.log(event);
        setScheduleDetails(event);
        setOpenUnavailabilityDetail(true);
    }

    const updateMeeting = (event, newValue) => {
        (async () => {
            setUpdateInProgress(true)
            const meeting_id = meetingDetails['meeting_id'];
            var form_data = new FormData();
            form_data.append('name', meetingDetails['name'])
            form_data.append('description', meetingDetails['description'])
            form_data.append('start_at', moment(meetingDetails['start_at']).format('YYYY-MM-DD HH:mm:ss'))
            form_data.append('end_at', moment(meetingDetails['end_at']).format('YYYY-MM-DD HH:mm:ss'))
            form_data.append('created_by', meetingDetails['meeting_creator_id'])
            form_data.append('room_id', meetingDetails['room_id'])

            const requestOptions = {
                method: 'PUT',
                body: form_data
            };
            const response = await fetch(`http://127.0.0.1:5000/waza/meeting/${meeting_id}?user_id=1`, requestOptions);
            const data = await response.json();
            console.log(data)
            getMeetings();
            setOpenMeetingDetail(false);
            setUpdateInProgress(false);
        })();
    }

    useEffect(() => {
        // initial value
        modifyMeetingForm('created_by', 1);
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
                let start_at = moment(selected['start']).format('MMM DD YYYY HH:mm:ss');
                let end_at = moment(selected['end']).format('MMM DD YYYY HH:mm:ss');
                onChangeDateRangeValue([start_at, end_at]);
                modifyMeetingForm('start_at', moment(selected['start']).format('YYYY-MM-DD HH:mm:ss'));
                modifyMeetingForm('end_at', moment(selected['end']).format('YYYY-MM-DD HH:mm:ss'));

                setOpen(true);
            }}
            onSelectEvent={(selected) => {
                if (selected['resources']['type'] === 'unavailable') getScheduleDetails(selected)
                else getMeetingDetails(selected['resources']['meeting_id'], selected['resources']['room_id']);
            }}
        >

        </Calendar>
        {/*Create a new meeting*/}
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
                            onChange={onChangeDateRangeValue}
                            value={dateRangeValue}
                        />
                    </Grid.Row>
                    <Grid.Row>
                        <Button onClick={() => {
                            let start_at = moment(dateRangeValue[0]).format('YYYY-MM-DD HH:mm:ss');
                            let end_at = moment(dateRangeValue[1]).format('YYYY-MM-DD HH:mm:ss');
                            modifyMeetingForm('start_at', start_at);
                            modifyMeetingForm('end_at', end_at);

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
                            <Form.Field disabled={roomsAvailable.length === 0} required>
                                <label>Meeting Name</label>
                                <input placeholder='Meeting Name' onChange={(event) => {
                                    event.preventDefault();
                                    modifyMeetingForm('name', event.target.value)
                                }}/>
                            </Form.Field>
                            <Form.Field disabled={roomsAvailable.length === 0} required>
                                <label>Meeting Description</label>
                                <input placeholder='Meeting Description' onChange={(event) => {
                                    event.preventDefault();
                                    modifyMeetingForm('description', event.target.value)
                                }}/>
                            </Form.Field>
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
                            <Button onClick={createMeeting} disabled={roomsAvailable.length === 0}
                                    color={'green'}>Create
                                Meeting</Button>
                        </Form>
                    </Grid.Row>
                </Grid>


            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpen(false)}>X</Button>
            </Modal.Actions>
        </Modal>
        {/*Create a new unavailability*/}
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
                        <Form>
                            <Button onClick={createUnavailability}
                                    color={'green'}>Create Unavailability</Button>
                        </Form>
                    </Grid.Row>
                </Grid>


            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpenCreateUnavailability(false)}>X</Button>
            </Modal.Actions>
        </Modal>
        {/*Meeting Details*/}
        <Modal
            centered={false}
            open={openMeetingDetail}
            onClose={() => setOpenMeetingDetail(false)}
            onOpen={() => setOpenMeetingDetail(true)}
        >
            <Dimmer active={deleteInProgress} inverted>
                <Loader inverted>Deleting</Loader>
            </Dimmer>
            <Dimmer active={updateInProgress} inverted>
                <Loader inverted>Updating</Loader>
            </Dimmer>
            <Modal.Header>Meeting Details</Modal.Header>
            <Modal.Content>
                <Grid columns={2} padded>
                    <Grid.Row>
                        <Grid.Column>
                            <Form>
                                <Card fluid>
                                    <Card.Content>
                                        <Form.Field>
                                            <input placeholder='Meeting Name' defaultValue={meetingDetails['name']}
                                                   onChange={(event) => {
                                                       event.preventDefault();
                                                       modifyMeetingDetails('name', event.target.value);
                                                   }}/>
                                        </Form.Field>
                                    </Card.Content>


                                    {/*<Card.Content header={meetingDetails['name']}/>*/}
                                    <Card.Content>
                                        <p>
                                            <Form.Field>
                                                <input placeholder='Meeting Description'
                                                       defaultValue={meetingDetails['description']}
                                                       onChange={(event) => {
                                                           event.preventDefault();
                                                           modifyMeetingDetails('description', event.target.value);
                                                       }}/>
                                            </Form.Field>
                                            {/*<b>Description:</b> {meetingDetails['description']}*/}
                                            <br/>
                                            <br/>
                                            <b>Start
                                                At:</b> {(moment(meetingDetails['start_at']).format('dddd, MMMM Do YYYY, h:mm a'))}
                                            <br/>
                                            <b>End
                                                At:</b> {(moment(meetingDetails['end_at']).format('dddd, MMMM Do YYYY, h:mm a'))}
                                        </p>
                                    </Card.Content>
                                </Card>

                                <Button onClick={updateMeeting} fluid>Update</Button>
                                <br></br>
                                <Button negative onClick={deleteMeeting}>Delete Meeting</Button>
                            </Form>
                        </Grid.Column>
                        <Grid.Column>
                            <Card fluid>
                                <Card.Content>
                                    <Card.Header>Created By</Card.Header>
                                </Card.Content>
                                <Card.Content>

                                    <Feed>
                                        <Container>
                                            <Feed.Event>
                                                <Feed.Content>
                                                    <Feed.Summary>
                                                        <b>{meetingDetails['meeting_creator_first_name']} {meetingDetails['meeting_creator_last_name']}</b>
                                                    </Feed.Summary>
                                                    <Feed.Content>
                                                        {meetingDetails['meeting_creator_email']}
                                                    </Feed.Content>
                                                    <Feed.Extra>
                                                        {meetingDetails['meeting_creator_phone']}
                                                    </Feed.Extra>
                                                </Feed.Content>
                                            </Feed.Event>
                                        </Container>
                                    </Feed>
                                </Card.Content>
                            </Card>
                            <Card fluid>
                                <Card.Content>
                                    <Card.Header>Invitees</Card.Header>
                                </Card.Content>
                                <Card.Content>

                                    <Feed>
                                        {meetingInvitees.map(({
                                                                  end_at,
                                                                  meeting_creator_email,
                                                                  meeting_creator_first_name,
                                                                  meeting_creator_last_name,
                                                                  meeting_creator_id,
                                                                  meeting_creator_phone,
                                                                  invitee_user_email,
                                                                  invitee_user_first_name,
                                                                  invitee_user_id,
                                                                  invitee_user_last_name,
                                                                  invitee_user_phone,
                                                                  meeting_id,
                                                                  start_at,
                                                                  name,
                                                                  description,
                                                                  invitee_id
                                                              }) => (
                                            <Container>
                                                <Feed.Event>

                                                    <Feed.Content>
                                                        <Feed.Summary>
                                                            <b>{invitee_user_first_name} {invitee_user_last_name}</b>
                                                        </Feed.Summary>
                                                        <Feed.Content>
                                                            {invitee_user_email}
                                                        </Feed.Content>
                                                        <Feed.Extra>
                                                            {invitee_user_phone}
                                                        </Feed.Extra>
                                                    </Feed.Content>
                                                    <Feed.Label>
                                                        <Button negative onClick={() => deleteInvitee(invitee_id)} circular icon='delete' />
                                                    </Feed.Label>
                                                </Feed.Event>
                                                <Divider/>
                                            </Container>
                                        ))}


                                    </Feed>
                                </Card.Content>
                            </Card>
                        </Grid.Column>

                    </Grid.Row>
                    <Grid.Row>
                    </Grid.Row>
                    <Grid.Row>
                    </Grid.Row>
                </Grid>


            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpenMeetingDetail(false)}>X</Button>
            </Modal.Actions>
        </Modal>
        {/*Unavailability Details*/}
        <Modal
            centered={false}
            open={openUnavailabilityDetail}
            onClose={() => setOpenUnavailabilityDetail(false)}
            onOpen={() => setOpenUnavailabilityDetail(true)}
        >
            <Dimmer active={deleteInProgressUnavailability} inverted>
                <Loader inverted>Deleting</Loader>
            </Dimmer>
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

                                <Button negative onClick={deleteUnavailability}>Delete Unavailability</Button>
                            </Form>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>


            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpenMeetingDetail(false)}>X</Button>
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
                    setOpenCreateUnavailability(true)
                }}
            > Mark as unavailable</Button>
        </Container>
    </Container>


}

export default BookMeeting;
