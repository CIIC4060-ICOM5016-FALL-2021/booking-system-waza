import React, {useState, useEffect} from 'react';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import {Divider, Header, Icon, Grid, Table} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";


function BookMeeting() {
    const [hourData, setHourData] = useState([]);
    const [bookedUserData, setBookedUserData] = useState([]);
    const [bookedRoomData, setBookedRoomData] = useState([]);

    useEffect(() => {
        fetch("https://guarded-hamlet-30872.herokuapp.com/waza/statistics/global/busiest-hours")
            .then(res => res.json())
            .then(
                (result) => {
                    setHourData(result)
                },
                // (error) => {
                //     this.setState({
                //         isLoaded: true,
                //         error
                //     });
                // }
            )
        fetch("https://guarded-hamlet-30872.herokuapp.com/waza/statistics/global/most-booked-users")
            .then(res => res.json())
            .then(
                (result) => {
                    setBookedUserData(result)
                },
            )
        fetch("https://guarded-hamlet-30872.herokuapp.com/waza/statistics/global/most-booked-rooms")
            .then(res => res.json())
            .then(
                (result) => {
                    setBookedRoomData(result)
                },
            )
    }, [])


    return <Grid centered stackable columns={2} padded>
        <Grid.Row>
            <Header as='h2'>
                <Icon name='line graph' />
                <Header.Content>Global Statistics</Header.Content>
            </Header>
        </Grid.Row>
        <Grid.Column>
            <Divider horizontal>
                <Header as='h4'>
                    <Icon name='clock'/>
                    Busiest Hours
                </Header>
            </Divider>
            <BarChart width={730} height={250} data={hourData}>
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis dataKey="meeting_hour"/>
                <YAxis/>
                <Tooltip/>
                <Legend/>
                <Bar dataKey="count" fill="#82ca9d"/>
            </BarChart>
            <Table striped>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell
                        >
                            Meeting Hour
                        </Table.HeaderCell>
                        <Table.HeaderCell
                        >
                            Count
                        </Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {hourData.map(({meeting_hour, count}) => (
                        <Table.Row>
                            <Table.Cell>{meeting_hour}</Table.Cell>
                            <Table.Cell>{count}</Table.Cell>
                        </Table.Row>
                    ))}
                </Table.Body>
            </Table>
        </Grid.Column>
        <Grid.Column>
            <Divider horizontal>
                <Header as='h4'>
                    <Icon name='users'/>
                    Most Booked Users
                </Header>
            </Divider>
            <BarChart width={730} height={250} data={bookedUserData}>
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis dataKey="email" interval={0} angle={30} dx={20} dy={30} height={75}/>
                <YAxis/>
                <Tooltip/>
                <Legend/>
                <Bar dataKey="count" fill="#82ca9d"/>
            </BarChart>
            <Table striped>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>
                            First Name
                        </Table.HeaderCell>
                        <Table.HeaderCell>
                            Last Name
                        </Table.HeaderCell>
                        <Table.HeaderCell>
                            Email
                        </Table.HeaderCell>
                        <Table.HeaderCell>
                            Phone
                        </Table.HeaderCell>
                        <Table.HeaderCell>
                            Count
                        </Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {bookedUserData.map(({count, email, first_name, last_name, phone}) => (
                        <Table.Row>
                            <Table.Cell>{first_name}</Table.Cell>
                            <Table.Cell>{last_name}</Table.Cell>
                            <Table.Cell>{email}</Table.Cell>
                            <Table.Cell>{phone}</Table.Cell>
                            <Table.Cell>{count}</Table.Cell>
                        </Table.Row>
                    ))}
                </Table.Body>
            </Table>
        </Grid.Column>
        <Grid.Column>
            <Divider horizontal>
                <Header as='h4'>
                    <Icon name='building'/>
                    Most Booked Rooms
                </Header>
            </Divider>
            <BarChart width={730} height={250} data={bookedRoomData}>
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis dataKey="room_name"/>
                <YAxis/>
                <Tooltip/>
                <Legend/>
                <Bar dataKey="count" fill="#82ca9d"/>
            </BarChart>
            <Table striped>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell>
                            Department
                        </Table.HeaderCell>
                        <Table.HeaderCell>
                            Room
                        </Table.HeaderCell>
                        <Table.HeaderCell>
                            Room Type
                        </Table.HeaderCell>
                        <Table.HeaderCell>
                            Count
                        </Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {bookedRoomData.map(({count, department_name, room_name, room_type}) => (
                        <Table.Row>
                            <Table.Cell>{department_name}</Table.Cell>
                            <Table.Cell>{room_name}</Table.Cell>
                            <Table.Cell>{room_type}</Table.Cell>
                            <Table.Cell>{count}</Table.Cell>
                        </Table.Row>
                    ))}
                </Table.Body>
            </Table>
        </Grid.Column>

    </Grid>
}

export default BookMeeting;
