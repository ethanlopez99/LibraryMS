import React, { useState } from "react";
import "./LoginScreen.css";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import axios from "axios";

import login_background from "../../assets/images/login_background.jpg";
// Validation schema created, for use in Formik form to make sure no empty fields
const validationSchema = Yup.object().shape({
  username: Yup.string().required("Required").label("Username"),
  password: Yup.string().required("Required").label("Password"),
});

const LoginScreen = ({ setUserToken }) => {
  // Defines errorMessage, for future errors
  const [errorMessage, setErrorMessage] = useState();

  // Handles login, taking in username and password from form
  const handleLogin = async ({ username, password }) => {
    // Creates user attempt object, to make post request cleaner
    const userAttempt = {
      username: username,
      password: password,
    };
    try {
      // Make post request with user data to the specified login endpoint
      const response = await axios.post(
        "http://127.0.0.1:8000/admins/login",
        userAttempt
      );
      // If user has been verified by API, status will be 200.
      if (response.status === 200) {
        // Populate user token with token provided by API
        setUserToken(response.data.access_token);
        // Remove any error messages if present
        setErrorMessage(null);
      }
    } catch (error) {
      // Set error message
      setErrorMessage(error.response.data.detail);
      // Log error message to console for further information
      console.error(error);
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
            {/* Error message is shown if it has been set by the login function */}
            {errorMessage && <div style={{ color: "red" }}>{errorMessage}</div>}
            <button type="submit" className="app_login-form_submit">
              Login
            </button>
          </Form>
        </Formik>
      </div>
    </div>
  );
};

export default LoginScreen;
