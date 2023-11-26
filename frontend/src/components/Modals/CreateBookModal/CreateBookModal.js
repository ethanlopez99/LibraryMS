import React, { useState } from "react";
import axios from "axios";
import { Formik, Form, Field, ErrorMessage } from "formik";

import * as Yup from "yup";

import "./CreateBookModal.css";

import { IoCloseOutline } from "react-icons/io5";

const CreateBookModal = ({
  setCreateBookModalShow,
  userToken,
  getNumberOfBooks,
}) => {
  const [message, setMessage] = useState(false);

  const validationSchema = Yup.object().shape({
    book_name: Yup.string().required("Required").label("Book Name"),
    author: Yup.string().required("Required").label("Author"),
  });

  const handleSubmit = async (values, { resetForm }) => {
    const new_book = { title: values.book_name, author: values.author };
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/books/new",
        new_book,
        { headers: { Authorization: `Bearer ${userToken}` } }
      );
      getNumberOfBooks();
      resetForm();
      setMessage({
        message: `New Book ${response.data.title} created with id ${response.data.id}`,
        color: "green",
      });
    } catch (error) {
      setMessage({
        message: "Unable to create book. Please try again",
        color: "red",
      });
      console.log(error);
    }
  };

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
          validationSchema={validationSchema}
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
              <ErrorMessage name="book_name" component="div" />
            </div>
            <div className="app_login-form_field_container">
              <Field
                type="text"
                id="author"
                name="author"
                placeholder="Author"
                className="app_login-form_input_field"
              />
              <ErrorMessage name="author" component="div" />
            </div>
            <button type="submit" className="app_login-form_submit">
              Create New Book
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

export default CreateBookModal;
