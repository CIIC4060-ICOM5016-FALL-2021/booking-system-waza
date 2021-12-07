import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views} from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Tab} from "semantic-ui-react";
import BookMeeting from "./BookMeeting";
import Schedule from "./Schedule";
import RoomSchedule from "./RoomSchedule";
import UserStatistics from "./UserStatistics";
import UserInfo from "./UserInfo";

function UserView() {
    const [isAuth, setIsAuth] = useState(localStorage.getItem('user_id') !== null)
    const panes = [
        {
            menuItem: 'Booking', render: () => <Tab.Pane active={isAuth}><BookMeeting/></Tab.Pane>
        },
        {
            menuItem: 'Schedule', render: () => <Tab.Pane active={isAuth}><Schedule/></Tab.Pane>
        },
        {
            menuItem: 'Room Management', render: () => <Tab.Pane active={isAuth}><RoomSchedule/></Tab.Pane>
        },
        {
            menuItem: 'User Statistics', render: () => <Tab.Pane active={isAuth}><UserStatistics/></Tab.Pane>
        },
        {
            menuItem: 'User Info', render: () => <UserInfo/>
        }
    ]

    return <Tab panes={panes}/>

}

export default UserView;
