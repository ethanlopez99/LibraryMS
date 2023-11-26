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
  const [message, setMessage] = useState(false);

  const validationSchema = Yup.object().shape({
    lender_name: Yup.string().required("Required").label("Book Name"),
  });

  const handleSubmit = async (values) => {
    const new_book = { lender_name: values.lender_name };
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/lenders/new",
        new_book,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );
      getNumberOfLenders();
      console.log(response);
      setMessage({
        message: `New Lender ${response.data.lender_name} created with id ${response.data.id}`,
        color: "green",
      });
    } catch (error) {}
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
