/*
Copyright (C) 2017 Semester.ly Technologies, LLC

Semester.ly is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Semester.ly is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
*/

import PropTypes from 'prop-types';
import React from 'react';
// import ClickOutHandler from 'react-onclickout';
// import uniq from 'lodash/uniq';
// import Clipboard from 'clipboard';

class Comment extends React.Component {
  // constructor(props) {
  //   super(props);
  // }
  render() {
    const commentContent = (
      <div className="comment-content">
        <h3>{ this.props.content }</h3>
      </div>
    )
    const profilePic = (
      <div
        className="social-pro-pic"
        style={{backgroundImage: 'url(https://lh6.googleusercontent.com/-iqNXPUCvgTk/AAAAAAAAAAI/AAAAAAAAAIU/IMUYG8om_Y4/photo.jpg?sz=50)', margin: '5px', zIndex: '2' }}
      />
    )
    const commentData = (
      <div className="comment-user-data">
        <h4>{ profilePic }</h4>
        <h2>{ this.props.writer }<br/> {this.props.date}</h2>
      </div>
    )
    return (<div
      className="comment-slot"
    >
      { commentData }
      { commentContent }
    </div>);
  }
}

Comment.defaultProps = {
  content: null,
  writer: null,
  slots: null,
  date: null,
};

Comment.propTypes = {
  content: PropTypes.string,
  writer: PropTypes.string,
  date: PropTypes.string,
};

export default Comment;
