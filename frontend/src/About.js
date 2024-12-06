import React from "react";
import { Container, Row, Col, Image, Card } from 'react-bootstrap';
import eye from './components/ankh.png';

const teamMembers = [
  { name: "Akshay S", role: "Developer" },
  { name: "Nitish Kumar Mahto", role: "Developer" },
  { name: "Sanjay Kandpal", role: "Developer" }
];

const About = () => {
  return (
    <Container className="py-5">
      <Row className="justify-content-center mb-5">
        <Col xs={12} md={8} lg={6} className="text-center">
          <Image src={eye} alt="MoodTunes Logo" fluid style={{maxHeight: "180px"}} className="mb-4" />
          <h1 className="display-4 mb-4">About MoodTunes</h1>
        </Col>
      </Row>
      
      <Row className="justify-content-center mb-5">
        <Col xs={12} md={10} lg={8}>
          <Card bg="dark" text="white" className="shadow">
            <Card.Body>
              <Card.Text className="lead">
                This project focuses on music for all emotions. Whether you're happy, sad, or suffering from a heartbreak, 
                our app doesn't need to be told anything. It reads your emotions like a friend and plays a song to soothe your heart.
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="justify-content-center">
        <Col xs={12} md={10} lg={8}>
          <h2 className="text-center mb-4">Our Team</h2>
          <Row>
            {teamMembers.map((member, index) => (
              <Col key={index} xs={12} md={4} className="mb-4">
                <Card bg="dark" text="white" className="h-100 shadow">
                  <Card.Body className="d-flex flex-column justify-content-center align-items-center">
                    <Card.Title>{member.name}</Card.Title>
                    <Card.Text>{member.role}</Card.Text>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Col>
      </Row>
    </Container>
  );
}

export default About;