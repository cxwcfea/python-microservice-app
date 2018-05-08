import React from 'react';

const addUser = (props) => (
  <form onSubmit={(event) => props.onUserAdded(event)}>
    <div className="form-group">
      <input
        name="username"
        className="form-control input-lg"
        type="text"
        placeholder="Enter a username"
        required
        value={props.username}
        onChange={props.onInputChange}
      />
    </div>
    <div className="form-group">
      <input
        name="email"
        className="form-control input-lg"
        type="email"
        placeholder="Enter an email address"
        required
        value={props.email}
        onChange={props.onInputChange}
      />
    </div>
    <input
      type="submit"
      className="btn btn-primary btn-lg btn-block"
      value="Submit"
    />
  </form>
);

export default addUser;
