import React from 'react';
import { useEffect } from 'react';
import { Container, Button, Navbar, Row, Col } from 'react-bootstrap';
import styles from './Manage.module.scss';


const Items = (props) => {
    const getStatusCss = (currentTime, polledTime) => {
        const statusMap = {
            true: 'statusGreen',
            false: 'statusRed'
        }
        return statusMap[currentTime - polledTime < 60];
    }
    const getItem = (name, polledTime, currentTime) => {
        console.log(name, polledTime, currentTime);
        return (
        <Row className={styles.element} xs="3">
            <Col>{name}</Col>
            <Col>
                <div className={styles[`status--${getStatusCss(currentTime, polledTime)}`]}></div>
            </Col>
            <Col>
                <Button variant="danger">Delete</Button>
            </Col>

        </Row>
        );
    }
    return (
        <div>
            <Row className={styles.header} xs="3">
                <Col>Name</Col>
                <Col>Status</Col>
                <Col></Col>
            </Row>
            {props.data.data && props.data.data.map(val => getItem(val.name, val.polled_time, props.data.current_time))}
        </div>
    ) 
}

const Manage = () => {
    const [data, setData] = React.useState({});
    const logOut = () => {
        console.log('logout');
    }
    const fetchData = () => {
        fetch('/rpi/manage/data')
            .then(res => res.json())
            .then(data => { 
                setData(data);
            })
            .catch(err => console.log(err));
    }
    useEffect(() => {
        fetchData();
        const interval = setInterval(() => {
            fetchData();
        }, 5000);

        return () => clearInterval(interval);
      }, [])

    return (
        <>
            <Navbar expand="lg" bg="dark" data-bs-theme="dark" className="bg-body-tertiary">
                <Container fluid>
                    <Navbar.Brand>Rpi remote server</Navbar.Brand>
                    <Button variant="danger" onClick={logOut}>Logout</Button>
                </Container>
            </Navbar>
            <Container className={styles.mainContainer}>
                <Container className={styles.dataContainer}>
                    <Items data={data}/>
                </Container>
            </Container>
        </>
    );
}

export default Manage;