import React, { useState } from "react";
import axios from "axios";
import * as Yup from "yup";

import { Formik, Form, Field, ErrorMessage, useFormikContext } from "formik";

import "./CreateLenderModal.css";

import { IoCloseOutline } from "react-icons/io5";

const CreateLenderModal = ({
  setCreateLenderModalShow,
  userToken,
  getNumberOfLenders,
}) => {
  // define message for future use
  const [message, setMessage] = useState(false);

  // new validation schema for formik form
  const validationSchema = Yup.object().shape({
    lender_name: Yup.string().required("Required").label("Book Name"),
  });

  // handles submit of new lender
  const handleSubmit = async (values, {resetForm}) => {
    // New lender values are stored in dictionary suitable for API request
    const new_lender = { lender_name: values.lender_name };
    try {
      const response = await axios.post(
      // post request is made to API endpoint
        "http://127.0.0.1:8000/lenders/new",
        new_lender,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );
      // if successful, update dashboard number of lenders and reset form
      getNumberOfLenders();
      resetForm();
      // add message to let user know successful creation and new lender id
      setMessage({
        message: `New Lender ${response.data.lender_name} created with id ${response.data.id}`,
        color: "green",
      });
    } catch (error) {
      // if error, let user know there was an issue with creation of book
      setMessage({
        message: "Unable to create lender. Please try again",
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
            onClick={() => setCreateLenderModalShow(false)}
            color="grey"
          />
        </div>
        <h1>Create New Lender</h1>
        <Formik
          initialValues={{ lender_name: "" }}
          onSubmit={handleSubmit}
          validationSchema={validationSchema}
        >
          <Form>
            <div className="app_login-form_field_container">
              <Field
                type="text"
                id="lender_name"
                name="lender_name"
                placeholder="Name"
                className="app_login-form_input_field"
              />
              {/* error message shown if input does not follow validation */}
              <ErrorMessage name="lender_name" component="div" />
            </div>
            <button type="submit" className="app_login-form_submit">
              Create New Lender
            </button>
            {message && (
              <h1 style={{ color: message.color }}>{message.message}</h1>
            )}
          </Form>
        </Formik>
      </div>
    </div>
  );
};

export default CreateLenderModal;
