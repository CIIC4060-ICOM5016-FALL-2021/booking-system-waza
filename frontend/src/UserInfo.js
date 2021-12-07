import React, {useState, useEffect} from 'react';
import {Divider,
	Header,
	Icon,
	Grid,
	Table,
	Card,
	Container,
	Button,
	Modal,
	Form,
	Dimmer,
       Loader} from "semantic-ui-react";

var role = 0;

function UserInfo() {

    const[info, setInfo] = useState([{
	'first_name': 'Fulano',
	'last_name': 'Detal',
	'email': 'fulano@email.com',
	'phone': '(555) 555-5555',
	'role' : 'Nobody'
    }]);

    const[toUpdate, setToUpdate] = useState(false);
    const[open, setOpen] = useState(false);
    const[userDetails, setUserDetails] = useState([]);


    const modifyUserInfo = (key, value) => {
	let tmp = userDetails;
	tmp[key] = value;
	setUserDetails(tmp);
	console.log(userDetails);
    }

    function getUserInfo(){
	let information = [];
	let role_name = '';
	fetch("http://127.0.0.1:5000/waza/user/10")
	    .then(res => res.json())
	    .then(
		(result) => {
		    window.role = result['role_id'];
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



    }

    // function updateUserInfo(firstName, lastName, email, phone){
    // 	let form_data = new FormData();
    // 	form_data.append('first_name', firstName);
    // 	form_data.append('last_name', lastName);
    // 	form_data.append('email', email);
    // 	form_data.append('phone', phone);
    // 	const requestOptions = {
    // 	    method: 'PUT',
    // 	    body: form_data
    // 	};
    // 	fetch('http://127.0.0.1:5000/waza/user/', requestOptions)
    // 	    .then(response =>
    // 		  response.json().then(data => ({
    //                   data: data,
    //                   status: response.status
    // 		  })
    // 				      ));
    
    // }

    function updateUserInfo()  {
        (async () => {
            setToUpdate(true);
            const user_id = userDetails['user_id'];
            var form_data = new FormData();
            form_data.append('role_id', window.role) //HARDCODED
            form_data.append('first_name', userDetails['first_name'])
            form_data.append('last_name',  userDetails['last_name'])
            form_data.append('email',  userDetails['email'])
            form_data.append('phone',  userDetails['phone'])

            const requestOptions = {
                method: 'PUT',
                body: form_data
            };
            const response = await fetch(`http://127.0.0.1:5000/waza/user/10`, requestOptions); //HARDCODED
            const data = await response.json();
            console.log(data)
            setToUpdate(false);
	    setOpen(false);
        })();
    }

    useEffect(() => {
	getUserInfo();
    }, [])



    return <Container>
	<Modal
            centered={false}
            open={open}
            onClose={() => setOpen(false)}
           e onOpen={() => setOpen(true)}
	>     <Dimmer active={toUpdate} inverted>
              <Loader inverted>Updating</Loader>
            </Dimmer>
            <Modal.Header>Update User Information</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                   Update your information.
    </Modal.Description>
    <Grid columnd={1} padded>
    <Grid.Row>
    <Grid.Column>
    <Form>
    <Card fluid>


	<Card.Content>
    <Form.Field>
	<input placeholder='First Name' defaultValue={userDetails['first_name']}
    onChange={(event) => {
	event.preventDefault();
	modifyUserInfo('first_name', event.target.value);
    }
    }
    />
    </Form.Field>
    </Card.Content>

	<Card.Content>
    <Form.Field>
    <input placeholder='Last Name'defaultValue={userDetails['last_name']}
    onChange={(event) => {
	event.preventDefault();
	modifyUserInfo('last_name', event.target.value);
    }
    }
    />
    </Form.Field>
	</Card.Content>

	<Card.Content>
    <Form.Field>
	<input placeholder='Email (ex. user@site.com)' defaultValue={userDetails['email']}
    onChange={(event) => {
	event.preventDefault();
	modifyUserInfo('email', event.target.value);
    }
    }
    
    />
    </Form.Field>
	</Card.Content>


	<Card.Content>
    <Form.Field>
    <input placeholder='Phone (ex. 555-555-5555)' defaultValue={userDetails['phone']}
    onChange={(event) => {
	event.preventDefault();
	modifyUserInfo('phone', event.target.value);
    }
    }
    />
    </Form.Field>
    </Card.Content>

    </Card>
    </Form>
    </Grid.Column>
    </Grid.Row>
    </Grid>
            </Modal.Content>
        <Modal.Actions>
	<Button onClick={() => updateUserInfo()}>Update</Button>
                <Button onClick={() => setOpen(false)}>Cancel</Button>
            </Modal.Actions>
        </Modal>



	<Grid centered stackable columns={2} padded>
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
        <Button onClick={() => setOpen(true)} fluid>Update</Button>   
        </Grid.Column>



    </Grid>
	</Container>
	
}

export default UserInfo;
