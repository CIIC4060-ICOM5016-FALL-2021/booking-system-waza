import React, {useState, useEffect} from 'react';
import {Divider, Header, Icon, Grid, Table, Card, Container, Button} from "semantic-ui-react";



function UserInfo() {
	const logged_uid = localStorage.getItem('user_id')
    const[info, setInfo] = useState([{
	'first_name': 'Fulano',
	'last_name': 'Detal',
	'email': 'fulano@email.com',
	'phone': '(555) 555-5555',
	'role' : 'Nobody'
    }]);

    useEffect(() => {
	let information = [];
	let role_name = '';
	fetch("http://127.0.0.1:5000/waza/user/"+logged_uid)
	    .then(res => res.json())
	    .then(
		(result) => {
		    switch(result['role_id']){
		    case 1:
			role_name = 'Department Staff';
			break;
		    case 2:
			role_name = 'Student';
			break;
		    case 3:
			role_name = 'Professor';
			break;
		    default:
			break;	
			    }
		    information.push({
			'first_name': result['first_name'],
			'last_name': result['last_name'],
			'email': result['email'],
			'phone': result['phone'],
			'role' : role_name
		    }
				    );
		    setInfo(information);
		},
	    );
    }, [])


	function removeActiveUser()
	{
// Remove data
        localStorage.removeItem(logged_uid);
		return window.location.href = "Home";
	}

    return <Grid centered stackable columns={2} padded>
        <Grid.Row>
            <Header as='h2'>
                <Icon name='user' />
                <Header.Content>User Info</Header.Content>
            </Header>
        </Grid.Row>
        <Grid.Column>
            <Divider horizontal>
        <Table striped>
        <Table.Header>
        <Table.Row>
        <Table.HeaderCell>First Name</Table.HeaderCell>
	<Table.HeaderCell>Last Name</Table.HeaderCell>
	<Table.HeaderCell>Email </Table.HeaderCell>
	<Table.HeaderCell>Phone</Table.HeaderCell>
	<Table.HeaderCell>Role</Table.HeaderCell>
	
    </Table.Row>
	</Table.Header>
	<Table.Body>
	{info.map(({first_name, last_name, email, phone, role}) => (
		<Table.Row>
		<Table.Cell>{first_name}</Table.Cell>
		<Table.Cell>{last_name}</Table.Cell>
		<Table.Cell>{email}</Table.Cell>
		<Table.Cell>{phone}</Table.Cell>
		<Table.Cell>{role}</Table.Cell>
		</Table.Row>

	))}

    </Table.Body>
    </Table>
            </Divider>
           
        </Grid.Column>



		<Button content='Logout' primary onClick={removeActiveUser}/>
    </Grid>
}

export default UserInfo;
