import React from 'react';
import { Container, Form, Button, FloatingLabel } from 'react-bootstrap';
import styles from './Login.module.scss';

function Login() {
    return (
        <Container className={styles['main-container']}>
            <Container className={styles['form-container']}>
                <Form>
                    <FloatingLabel
                        controlId="userName"
                        label="Username"
                        className="mb-2"
                    >
                        <Form.Control type="username" placeholder="Username" />
                    </FloatingLabel>
                    <FloatingLabel controlId="password" label="Password">
                        <Form.Control type="password" placeholder="Password" />
                    </FloatingLabel>
                    <Button variant="secondary" 
                            type="submit" 
                            className='submit-button'>
                        Login
                    </Button>
                </Form>
            </Container>
        </Container>
    );
}

export default Login;