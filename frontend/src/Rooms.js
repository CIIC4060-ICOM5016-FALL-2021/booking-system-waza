import React, {useState, useEffect} from 'react';
import {
    Divider,
    Header,
    Icon,
    Grid,
    Table,
    Card,
    Container,
    Button,
    Dimmer,
    Loader,
    Modal,
    Form, Select
} from "semantic-ui-react";
import moment from "moment";


function Rooms() {
    const logged_uid = localStorage.getItem('user_id')
    const [info, setInfo] = useState([{
        'room_name': 'Empty',
        'department_name': 'Nowhere',
        'capacity': 1,
        'room_type': 'Classroom',
        'id': 1,
        'department_id': 1,
        'roomtype_id': 2
    }]);
    const [openCreateRoom, setOpenCreateRoom] = useState(false);
    const [openUpdateRoom, setOpenUpdateRoom] = useState(false);
    const [newRoomInformation, setNewRoomInformation] = useState(new Map());
    const [updatedRoomInformation, setNewUpdatedInformation] = useState(new Map());
    const [deleteInProgress, setDeleteInProgress] = useState(false);
    const [roleDisabled, setRoleDisabled] = useState(false);

    const modifyRoomForm = (key, value) => {
        newRoomInformation.set(key, value)
    }

    const modifyRoomUpdateForm = (key, value) => {
        updatedRoomInformation.set(key, value)
    }

    const prepareForUpdate = (room_id, room_name, capacity, roomtype_id, department_id, department_name, room_type) => {
        updatedRoomInformation.set('room_id', room_id);
        updatedRoomInformation.set('name', room_name);
        updatedRoomInformation.set('capacity', capacity);
        updatedRoomInformation.set('roomtype_id', roomtype_id);
        updatedRoomInformation.set('department_id', department_id);
        updatedRoomInformation.set('department_name', department_name);
        updatedRoomInformation.set('roomtype_name', room_type)
        setOpenUpdateRoom(true);
    }

    const departments = [
        {
            key: '1',
            text: 'Industrial Engineering',
            value: '1',
        },
        {
            key: '2',
            text: 'Computer Engineering',
            value: '2',
        },
        {
            key: '3',
            text: 'Electrical Engineering',
            value: '3',
        },
        {
            key: '4',
            text: 'Business Administration',
            value: '4',
        },
        {
            key: '5',
            text: 'Computer Science and Engineering',
            value: '5',
        },
        {
            key: '6',
            text: 'Math',
            value: '6',
        },
        {
            key: '7',
            text: 'Physics',
            value: '7',
        },
        {
            key: '8',
            text: 'Social Sciences',
            value: '8',
        },
        {
            key: '9',
            text: 'Biology',
            value: '9',
        }
    ]

    const room_types = [
        {
            key: '1',
            text: 'Classroom',
            value: '1',
        },
        {
            key: '2',
            text: 'Laboratory',
            value: '2',
        },
        {
            key: '3',
            text: 'Amphitheatre',
            value: '3',
        }
    ]

    function getRooms() {
        let rooms = [];
        let department_name = '';
        let room_type = '';
        fetch("https://guarded-hamlet-30872.herokuapp.com/waza/room")
            .then(res => res.json())
            .then(
                (result) => {
                    for (var r in result) {


                        switch (result[r]['department_id']) {
                            case 1:
                                department_name = "Industrial Engineering";
                                break;
                            case 2:
                                department_name = "Computer Engineering";
                                break;
                            case 3:
                                department_name = "Electrical Engineering";
                                break;
                            case 4:
                                department_name = "Business Administration";
                                break;
                            case 5:
                                department_name = "Computer Science and Engineering";
                                break;
                            case 6:
                                department_name = "Math";
                                break;
                            case 7:
                                department_name = "Physics";
                                break;
                            case 8:
                                department_name = "Social Sciences";
                                break;
                            case 9:
                                department_name = "Biology";
                                break;

                        }

                        switch (result[r]['roomtype_id']) {
                            case 1:
                                room_type = 'Classroom';
                                break;
                            case 2:
                                room_type = 'Laboratory';
                                break;
                            case 3:
                                room_type = 'Amphitheatre';
                                break;

                        }

                        rooms.push({
                            'room_name': result[r]['name'],
                            'department_name': department_name,
                            'capacity': result[r]['capacity'],
                            'room_type': room_type,
                            'id': result[r]['id'],
                            'department_id': result[r]['department_id'],
                            'roomtype_id': result[r]['roomtype_id']
                        });


                    }
                    setInfo(rooms);

                }
            );

    }

    const user_info = () => {
        fetch(`https://guarded-hamlet-30872.herokuapp.com/waza/user/${logged_uid}`)
            .then(res => res.json())
            .then(
                (result) => {
                    if (result['role_id'] === 1) setRoleDisabled(false)
                    else setRoleDisabled(true)
                },
            ).catch(setRoleDisabled(true));
    }

    useEffect(() => {
        user_info()
        getRooms();
    }, [])

    const createRoom = (event, newValue) => {
        (async () => {
            let form_data = new FormData();
            for (let [key, value] of newRoomInformation) {
                form_data.append(key, value);
            }

            const requestOptions = {
                method: 'POST',
                body: form_data
            };
            const response = await fetch('https://guarded-hamlet-30872.herokuapp.com/waza/room', requestOptions)
                .then(response =>
                    response.json().then(data => ({
                            data: data,
                            status: response.status
                        })
                    ).then(res => {
                        getRooms();
                        setOpenCreateRoom(false)
                    }))
                .catch(error => {
                    window.alert('Invalid Information.')
                });
            // const data = await response.json();

        })();
    }

    const updateRoom = (event, newValue) => {
        (async () => {
            const room_id = updatedRoomInformation.get('room_id')
            let form_data = new FormData();
            form_data.append('capacity', updatedRoomInformation.get('capacity'));
            form_data.append('department_id', updatedRoomInformation.get('department_id'));
            form_data.append('roomtype_id', updatedRoomInformation.get('roomtype_id'));
            form_data.append('name', updatedRoomInformation.get('name'));

            const requestOptions = {
                method: 'PUT',
                body: form_data
            };
            const response = await fetch(`https://guarded-hamlet-30872.herokuapp.com/waza/room/${room_id}`, requestOptions)
                .then(response =>
                    response.json().then(data => ({
                            data: data,
                            status: response.status
                        })
                    ).then(res => {
                        getRooms();
                        setOpenUpdateRoom(false)
                    }))
                .catch(error => {
                    window.alert('Invalid Information.')
                });
            // const data = await response.json();

        })();
    }

    const deleteRoom = (room_id) => {
        (async () => {
            setDeleteInProgress(true);
            const requestOptions = {
                method: 'DELETE',
            };
            const response = await fetch(`https://guarded-hamlet-30872.herokuapp.com/waza/room/${room_id}`, requestOptions)
                .then(response =>
                    response.json().then(data => ({
                            data: data,
                            status: response.status
                        })
                    ).then(res => {
                        setDeleteInProgress(false);
                        getRooms();
                    }))
                .catch(error => {
                    window.alert('Invalid Deletion.')
                    setDeleteInProgress(false);
                });
            // console.log(await response.json())

        })();
    }

    return <Grid centered stackable columns={2} padded>
        <Dimmer active={deleteInProgress} inverted>
            <Loader inverted>Deleting</Loader>
        </Dimmer>
        <Grid.Row>
            <Button
                fluid
                color={'green'}
                onClick={() => {
                    setOpenCreateRoom(true)
                }}
            >Create a Room</Button>
        </Grid.Row>
        <Grid.Row>
            <Header as='h2'>
                <Header.Content>Room</Header.Content>
            </Header>
        </Grid.Row>
        <Grid.Column>
            <Divider horizontal>
                <Table striped>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell>Room Name</Table.HeaderCell>
                            <Table.HeaderCell>Department Name</Table.HeaderCell>
                            <Table.HeaderCell>Capacity</Table.HeaderCell>
                            <Table.HeaderCell>Room Type</Table.HeaderCell>

                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {info.map(({
                                       room_name,
                                       department_name,
                                       capacity,
                                       room_type,
                                       id,
                                       department_id,
                                       roomtype_id
                                   }) => (
                            <Table.Row>
                                <Table.Cell>{room_name}</Table.Cell>
                                <Table.Cell>{department_name}</Table.Cell>
                                <Table.Cell>{capacity}</Table.Cell>
                                <Table.Cell>{room_type}</Table.Cell>
                                <Table.Cell><Button disabled={roleDisabled}
                                                    onClick={() => deleteRoom(id)}>DELETE</Button></Table.Cell>
                                <Table.Cell><Button disabled={roleDisabled}
                                                    onClick={() => prepareForUpdate(id, room_name, capacity, roomtype_id, department_id, department_name, room_type)}>UPDATE</Button></Table.Cell>
                            </Table.Row>

                        ))}

                    </Table.Body>
                </Table>
            </Divider>

        </Grid.Column>


        <Modal
            centered={false}
            open={openCreateRoom}
            onClose={() => setOpenCreateRoom(false)}
            onOpen={() => setOpenCreateRoom(true)}
        >
            <Modal.Header>Create Room</Modal.Header>
            <Modal.Content>
                <Grid columns={2} padded>
                    <Grid.Row>
                        <Grid.Column>
                            <Form>
                                <Form.Field required>
                                    <label>Room Name</label>
                                    <input placeholder='Room Name' onChange={(event) => {
                                        event.preventDefault();
                                        modifyRoomForm('name', event.target.value)
                                    }}/>
                                </Form.Field>
                                <Form.Field required>
                                    <label>Capacity</label>
                                    <input placeholder='Room Capacity' onChange={(event) => {
                                        event.preventDefault();
                                        modifyRoomForm('capacity', event.target.value)
                                    }}/>
                                </Form.Field>
                                <Form.Dropdown
                                    label={'Department'}
                                    required
                                    control={Select}
                                    options={departments}
                                    placeholder='Department'
                                    search
                                    searchInput={{id: 'form-select-control-room'}}
                                    onChange={(event, newValue) => modifyRoomForm('department_id', newValue.value)}
                                />
                                <Form.Dropdown
                                    label={'Room Types'}
                                    required
                                    control={Select}
                                    options={room_types}
                                    placeholder='Room Types'
                                    search
                                    searchInput={{id: 'form-select-control-room'}}
                                    onChange={(event, newValue) => modifyRoomForm('roomtype_id', newValue.value)}
                                />
                                <Button onClick={createRoom} color={'green'}>Create Room</Button>
                            </Form>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>


            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpenCreateRoom(false)}>X</Button>
            </Modal.Actions>
        </Modal>


        <Modal
            centered={false}
            open={openUpdateRoom}
            onClose={() => setOpenUpdateRoom(false)}
            onOpen={() => setOpenUpdateRoom(true)}
        >
            <Modal.Header>Update Room</Modal.Header>
            <Modal.Content>
                <Grid columns={2} padded>
                    <Grid.Row>
                        <Grid.Column>
                            <Form>
                                <Form.Field required>
                                    <label>Room Name</label>
                                    <input placeholder='Room Name' defaultValue={updatedRoomInformation.get('name')}
                                           onChange={(event) => {
                                               event.preventDefault();
                                               modifyRoomUpdateForm('name', event.target.value)
                                           }}/>
                                </Form.Field>
                                <Form.Field required>
                                    <label>Capacity</label>
                                    <input placeholder='Room Capacity'
                                           defaultValue={updatedRoomInformation.get('capacity')} onChange={(event) => {
                                        event.preventDefault();
                                        modifyRoomUpdateForm('capacity', event.target.value)
                                    }}/>
                                </Form.Field>
                                <Form.Dropdown
                                    label={updatedRoomInformation.get('department_name')}
                                    required
                                    control={Select}
                                    options={departments}
                                    placeholder='Department'
                                    search
                                    searchInput={{id: 'form-select-control-room'}}
                                    onChange={(event, newValue) => modifyRoomUpdateForm('department_id', newValue.value)}
                                />
                                <Form.Dropdown
                                    label={updatedRoomInformation.get('roomtype_name')}
                                    required
                                    control={Select}
                                    options={room_types}
                                    placeholder='Room Types'
                                    search
                                    searchInput={{id: 'form-select-control-room'}}
                                    onChange={(event, newValue) => modifyRoomUpdateForm('roomtype_id', newValue.value)}
                                />
                                <Button onClick={updateRoom} color={'green'}>Update Room</Button>
                            </Form>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>


            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpenCreateRoom(false)}>X</Button>
            </Modal.Actions>
        </Modal>
    </Grid>
}

export default Rooms;
