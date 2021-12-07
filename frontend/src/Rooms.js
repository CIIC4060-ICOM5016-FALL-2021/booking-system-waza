import React, {useState, useEffect} from 'react';
import {Divider, Header, Icon, Grid, Table, Card, Container, Button} from "semantic-ui-react";



function Rooms() {
	const logged_uid = localStorage.getItem('user_id')
    const[info, setInfo] = useState([{
	'room_name': 'Empty',
	'department_name': 'Nowhere',
	'capacity': 1,
	'room_type': 'Classroom',
    }]);

    function getRooms(){
	let rooms = [];
	let department_name = '';
	let room_type = '';
	fetch("http://127.0.0.1:5000/waza/room")
	    .then(res => res.json())
	    .then(
		(result) => {
		    for(var r in result){


			switch(result[r]['department_id']){
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

			switch(result[r]['roomtype_id']){
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
			    'room_type': room_type
			    

			});


		
		    }
		    setInfo(rooms);
		    console.log(rooms);

		}
	    );
		
    }

    useEffect(() => {
	// let information = [];
	// let role_name = '';
	// fetch("http://127.0.0.1:5000/waza/user/"+logged_uid)
	//     .then(res => res.json())
	//     .then(
	// 	(result) => {
	// 	    // if(result['role_id'] == 3){
	// 	    // 	getRooms();}
	// 	    // else{
	// 	    // 	window.alert("You are not allowed to manage rooms.");
	// 	    // };
	// 	},
	//     );
	getRooms();
    }, [])


	function removeRoom()
    {
	

	}

    return <Grid centered stackable columns={2} padded>
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
	{info.map(({room_name, department_name, capacity, room_type}) => (
		<Table.Row>
		<Table.Cell>{room_name}</Table.Cell>
		<Table.Cell>{department_name}</Table.Cell>
		<Table.Cell>{capacity}</Table.Cell>
		<Table.Cell>{room_type}</Table.Cell>
		<Table.Cell><Button>DELETE</Button></Table.Cell>
		<Table.Cell><Button>UPDATE</Button></Table.Cell>
		</Table.Row>

	))}

    </Table.Body>
    </Table>
            </Divider>
           
        </Grid.Column>


    </Grid>
}

export default Rooms;
