import React, { useState } from 'react';
import { useEffect } from 'react';
import { Container, Button, Navbar, Row, Col } from 'react-bootstrap';
import styles from './Manage.module.scss';
import { ReactComponent as ReactLogo } from '../xicon.svg';
import { ReactComponent as RpiIcon } from '../rpi.svg';
import { redirectToLogin } from '../redirect';


const fetchData = async (token, setToken, onDataChanged) => {
    return fetch('/rpi/api/data', {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
        })
        .then(res => {
            if (res.status === 401) {
                redirectToLogin();
            }
            return res.json()
        })
        .then(data => {
            onDataChanged(data);
            data.access_token && setToken(data.access_token);
        })
        .catch(err => {console.log(err)});
}


const ItemList = ({ data, token, setToken, onDataChanged }) => {
    const deleteItem = (name) => () => {
        fetch('/rpi/api/data', {
            method: 'DELETE',
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({name: name}),
        }).then(
                res => fetchData(token, setToken, onDataChanged)
            )
          .catch(err => console.log(err));
    }
    const getItem = (name, polledTime, currentTime) => {
        const getStatusCss = (currentTime, polledTime) => {
            const statusMap = {
                true: 'statusGreen',
                false: 'statusRed'
            }
            return statusMap[currentTime - polledTime < 60];
        }

        return (
        <Row className={styles.element} xs="3" key={name}>
            <Col md={5}>{name}</Col>
            <Col md={5}>
                <div className={styles[`status--${getStatusCss(currentTime, polledTime)}`]}></div>
            </Col>
            <Col className={styles.xbutton} md={2}>
                <Button variant="outline-danger" 
                        onClick={deleteItem(name)}>
                    <ReactLogo />
                </Button>
            </Col>
        </Row>
        );
    }
    return (
        <div>
            <Row className={styles.header} xs="3">
                <Col md={5}>Name</Col>
                <Col md={5}>Status</Col>
                <Col md={2}></Col>
            </Row>
            {data.data && data.data
                .map(val => getItem(val.name, val.polled_time, data.current_time))}
        </div>
    ) 
}

const Manage = ({ setToken, token, removeToken }) => {
    const [data, setData] = useState({});
    token || redirectToLogin();

    const logOut = () => {
        fetch('/rpi/logout', {method: "POST"})
        .then(res => {
            removeToken();
            redirectToLogin();
        }).catch(err => console.log(err));
    }
    const onDataChanged = (data) => {
        setData(data);
    }
    useEffect(() => {
        fetchData(token, setToken, onDataChanged);
        const interval = setInterval(() => {
            fetchData(token, setToken, onDataChanged);
        }, 5000);
        return () => clearInterval(interval);
      }, [token, setToken])

    return (
        <>
            <Navbar expand="lg" bg="dark" data-bs-theme="dark" className="bg-body-tertiary">
                <Container fluid>
                    <Navbar.Brand><RpiIcon />Rpi remote server</Navbar.Brand>
                    <Button variant="danger" onClick={logOut}>Logout</Button>
                </Container>
            </Navbar>
            <Container className={styles.mainContainer}>
                <Container className={styles.dataContainer}>
                    <ItemList data={data} 
                              onDataChanged={onDataChanged} 
                              token={token} 
                              setToken={setToken}
                    />
                </Container>
            </Container>
        </>
    );
}

export default Manage;