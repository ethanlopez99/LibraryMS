import React, { useState } from "react";
import axios from "axios";
import { Formik, Form, Field } from "formik";

import "./CreateLenderModal.css";

import { IoCloseOutline } from "react-icons/io5";

const CreateLenderModal = ({
  setCreateLenderModalShow,
  userToken,
  getNumberOfLenders,
}) => {
  const [message, setMessage] = useState(false);

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
    } catch (error) {}
  };

  const handleReset = async () => {};

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
        <h1>Create New Book</h1>
        <Formik
          initialValues={{ lender_name: "" }}
          onSubmit={handleSubmit}
          //   validationSchema={validationSchema}
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
            </div>
            <button type="submit" className="app_login-form_submit">
              Create New Lender
            </button>
          </Form>
        </Formik>
        {message && <h1 style={{ color: message.color }}>{message.message}</h1>}
        <div className="modal_buttons">
          <button type="reset" onClick={handleReset}>
            Clear Fields
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateLenderModal;
