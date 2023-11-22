import React from "react";
import "./LoginScreen.css";

import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import axios from "axios";

import login_background from "../../assets/images/login_background.jpg";

const validationSchema = Yup.object().shape({
  username: Yup.string().required("Required").label("Username"),
  password: Yup.string().required("Required").label("Password"),
});

const LoginScreen = ({ setUserToken }) => {
  const handleLogin = async ({ username, password }) => {
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
    <div
      className="app_login"
      style={{ backgroundImage: `url(${login_background})` }}
    >
      <div className="app_login-form_container">
        <h1>Log In</h1>
        <Formik
          initialValues={{ username: "", password: "" }}
          onSubmit={handleLogin}
          validationSchema={validationSchema}
        >
          <Form>
            <div className="app_login-form_field_container">
              <Field
                type="text"
                id="username"
                name="username"
                placeholder="Username"
                className="app_login-form_input_field"
              />
            </div>
            <div className="app_login-form_field_container">
              <Field
                type="password"
                id="password"
                name="password"
                placeholder="Password"
                className="app_login-form_input_field"
              />
            </div>
            <button type="submit" className="app_login-form_submit">Login</button>
          </Form>
        </Formik>
      </div>
    </div>
  );
};

export default LoginScreen;
