import React, { useState } from "react";
import axios from "axios";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

import { IoCloseOutline } from "react-icons/io5";

import "./UpdatePasswordModal.css";
const validationSchema = Yup.object().shape({
  password: Yup.string().required("Required").label("Password"),
  repeat_password: Yup.string().required("Required").label("Password"),
});
const UpdatePasswordModal = ({
  userToken,
  setUserToken,
  setUpdatePasswordModalShow,
}) => {
  const [message, setMessage] = useState();

  const handleSubmit = async (values) => {
    if (values.password !== values.repeat_password) {
      setMessage({
        message: "Passwords do not match. Please try again.",
        color: "red",
      });
      return null;
    }
    const new_password = { password: values.password };
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/admins/update",
        new_password,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );
      if (response.status === 200) {
        setMessage({
          message: "Password updated successfully. You will be logged out now.",
          color: "green",
        });
        setTimeout(() => setUserToken(null), 2000);
      }
    } catch (error) {
      console.log(error);
      setMessage({
        message: "Error updating your password. Please try again later.",
        color: "red",
      });
    }
  };

  return (
    <div className="modal_bg">
      <div className="app_modal">
        <div className="app_modal-close">
          <IoCloseOutline
            size={50}
            onClick={() => setUpdatePasswordModalShow(false)}
            color="grey"
          />
        </div>
        <h1>Update Your Password</h1>
        <Formik
          initialValues={{ password: "", repeat_password: "" }}
          onSubmit={handleSubmit}
          validationSchema={validationSchema}
        >
          <Form className="password_form">
            <Field
              type="password"
              id="password"
              name="password"
              placeholder="New Password"
              className="app_login-form_input_field"
            />
            <Field
              type="password"
              id="repeat_password"
              name="repeat_password"
              placeholder="New Password (Again)"
              className="app_login-form_input_field"
            />
            <div className="modal_buttons">
              <button type="submit">Submit Return Request</button>
            </div>
          </Form>
        </Formik>
        {message && <h1 style={{ color: message.color }}>{message.message}</h1>}
      </div>
    </div>
  );
};

export default UpdatePasswordModal;
