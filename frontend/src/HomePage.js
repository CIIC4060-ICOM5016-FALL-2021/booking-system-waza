import React, {Component, useState} from 'react';
import {Button, Divider, Form, Grid, Header, Modal, Segment, Tab} from 'semantic-ui-react';



function HomePage() {
    const [open, setOpen] = useState(false);
    console.log(open);
    const handleChange = (event, newValue) => {
        setOpen(true);
    let signUp = false;
    }

    function addActiveUser(email,id)
    {
        window.alert(localStorage.getItem(email))
        // Add Data
        localStorage.setItem(email, id);

// Get data
//        window.alert(localStorage.getItem(email))
// // Remove data
//         localStorage.removeItem(email);
//         window.alert(localStorage.getItem(email))
    }

    //LOGIN
//---------------------------------------------------------------------------------------
     function UserAuthantication()
    {
        let un = document.getElementById("un").value;
        let pw = document.getElementById("pw").value;

        fetch('https://guarded-hamlet-30872.herokuapp.com/waza/user/'+un+'/'+pw)
            .then(response =>
            response.json().then(data => ({
                    data: data,
                    status: response.status
                })
            ).then(res => {
                let userID = res.data['id']
                addActiveUser(un,userID)
            }));
        return 0;

    }
//-----------------------------------------------------------------------------------------------

    //Register new user
    function register()
    {
        let role_id = document.getElementById("rid").value
        let firstName = document.getElementById("fn").value
        let lastName = document.getElementById("ln").value
        let email = document.getElementById("email").value
        let phone = document.getElementById("phone").value
        let password = document.getElementById("unpw").value

        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role_id: role_id,first_name: firstName, last_name: lastName, email:email,phone:phone, passwor: password })
        };

        fetch('https://guarded-hamlet-30872.herokuapp.com/waza/user/', requestOptions)
            .then(response =>
                response.json().then(data => ({
                        data: data,
                        status: response.status
                    })
                ).then(res => {
                    let userID = res.data['id']
                    addActiveUser(email,userID)
                }))
            .catch(error => {
                window.alert(error)
            });

    }
//-----------------------------------------------------------------------------------------------

    return (<Segment><Header dividing textAlign="center" size="huge">Welcome to DB Demo</Header>
            <Modal
                centered={false}
                open={open}
                onClose={() => setOpen(false)}
                onOpen={() => setOpen(true)}
            >
                <Modal.Header>Needs changing!</Modal.Header>
                <Modal.Content>
                    <Modal.Description>
                        This is a modal but it serves to show how buttons and functions can be implemented.
                    </Modal.Description>
                </Modal.Content>
                <Modal.Actions>
                    <Button onClick={() => setOpen(false)}>OK</Button>
                </Modal.Actions>
            </Modal>
            <Segment placeholder>

                <Grid columns={2} relaxed='very' stackable>
                    <Grid.Column>
                        <Form>
                            <Form.Input
                                icon='mail'
                                iconPosition='left'
                                label='Email'
                                placeholder='user@example.com'
                                id='un'
                            />
                            <Form.Input
                                icon='lock'
                                iconPosition='left'
                                label='Password'
                                type='password'
                                id='pw'
                            />
                            <Button content='Login' primary onClick={UserAuthantication}/>
                        </Form>
                    </Grid.Column>
                    <Grid.Column verticalAlign='middle'>
                        <Grid.Column>
                            <Form>
                                <Form.Input
                                    icon='mail'
                                    iconPosition='left'
                                    label='Email'
                                    placeholder='user@example.com'
                                    id='email'
                                /> <Form.Input
                                    icon='lock'
                                    iconPosition='left'
                                    label='Password'
                                    placeholder='Password'
                                    id='unpw'
                                />
                                <Form.Input
                                    icon='user'
                                    iconPosition='left'
                                    label='First Name'
                                    placeholder='John'
                                    id='fn'
                                />
                                <Form.Input
                                    label='Last Name'
                                    placeholder='         Doe'
                                    id='ln'
                                />
                                <Form.Input
                                    icon='phone'
                                    iconPosition='left'
                                    label='Phone'
                                    placeholder='787-939-6969'
                                    id='phone'
                                />
                                <Form.Input
                                    icon='men'
                                    iconPosition='left'
                                    label='Role'
                                    placeholder='e.g. 1'
                                    id='rid'
                                />
                                <Button content='Register' primary onClick={register}/>
                            </Form>
                        </Grid.Column>
                    </Grid.Column>
                </Grid>
                <Divider vertical>Or</Divider>
            </Segment>
        </Segment>
    )
}


export default HomePage;
