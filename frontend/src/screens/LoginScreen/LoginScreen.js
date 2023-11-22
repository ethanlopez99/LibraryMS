import React from "react";
import "./LoginScreen.css";

import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import axios from "axios";

const validationSchema = Yup.object().shape({
  username: Yup.string().required("Required").label("Username"),
  password: Yup.string().required("Required").label("Password"),
});

const LoginScreen = ({ setUserToken }) => {
  const handleLogin = async ({ username, password, setFieldError }) => {
    const userAttempt = {
      username: username,
      password: password,
    };
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/admins/login",
        userAttempt
      );
      if (response.status === 200) {
        setUserToken(response.data.access_token);
      }
    } catch (error) {
      if (error.response.status === 401) {
        console.log("Incorrect username or password"); // to add Formik error handling here
      }
      console.error(error.message);
    }
  };

  return (
    <div className="app_login">
      <Formik
        initialValues={{ username: "", password: "" }}
        onSubmit={handleLogin}
        validationSchema={validationSchema}
      >
        <Form>
          <div>
            <label htmlFor="username">Username</label>
            <Field
              type="text"
              id="username"
              name="username"
              placeholder="Username"
            />
          </div>
          <div>
            <label htmlFor="password">Password</label>
            <Field
              type="password"
              id="password"
              name="password"
              placeholder="Password"
            />
            <ErrorMessage name="password" component="div" />
          </div>
          <div>
            <button type="submit">Login</button>
          </div>
        </Form>
      </Formik>
    </div>
  );
};

export default LoginScreen;
