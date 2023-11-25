import React, { useState } from "react";
import axios from "axios";
import { Formik, Form, Field } from "formik";

import "./CreateBookModal.css";

import { IoCloseOutline } from "react-icons/io5";

const CreateBookModal = ({
  setCreateBookModalShow,
  userToken,
  getNumberOfBooks,
}) => {
  const [message, setMessage] = useState(false);

  const handleSubmit = async (values) => {
    const new_book = { title: values.book_name, author: values.author };
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/books/new",
        new_book,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );
      getNumberOfBooks();
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
            onClick={() => setCreateBookModalShow(false)}
            color="grey"
          />
        </div>
        <h1>Create New Book</h1>
        <Formik
          initialValues={{ book_name: "", author: "" }}
          onSubmit={handleSubmit}
          //   validationSchema={validationSchema}
        >
          <Form>
            <div className="app_login-form_field_container">
              <Field
                type="text"
                id="book_name"
                name="book_name"
                placeholder="Title"
                className="app_login-form_input_field"
              />
            </div>
            <div className="app_login-form_field_container">
              <Field
                type="text"
                id="author"
                name="author"
                placeholder="Author"
                className="app_login-form_input_field"
              />
            </div>
            <button type="submit" className="app_login-form_submit">
              Create New Book
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

export default CreateBookModal;
