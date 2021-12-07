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
import Rooms from "./Rooms";

function UserView() {
    const [isAuth, setIsAuth] = useState(localStorage.getItem('user_id') !== null)
    if(!isAuth) return window.location.href = "Home";
    const panes = [
        {
            menuItem: 'Booking', render: () => <Tab.Pane active={isAuth}><BookMeeting/></Tab.Pane>
        },
        {
            menuItem: 'User Schedule', render: () => <Tab.Pane active={isAuth}><Schedule/></Tab.Pane>
        },
        {
            menuItem: 'Room Schedule', render: () => <Tab.Pane active={isAuth}><RoomSchedule/></Tab.Pane>
        },
        {
            menuItem: 'User Statistics', render: () => <Tab.Pane active={isAuth}><UserStatistics/></Tab.Pane>
        },
        {
            menuItem: 'User Info', render: () => <UserInfo/>
        },
	{
	    menuItem: 'Room Management', render: () => <Rooms/>
	}
    ]

    return <Tab panes={panes}/>

}

export default UserView;
