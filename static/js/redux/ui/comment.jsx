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
import * as SemesterlyPropTypes from '../constants/semesterlyPropTypes';
import React from 'react';

class Comment extends React.Component {
  render() {
    const parsedDate = new Date(this.props.date).toDateString();
    const parsedTime = new Date(this.props.date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    const commentContent = (
      <div className="comment-content">
        <h3>{ this.props.content }</h3>
      </div>
    );
    const profilePic = (this.props.imageURL === '-1') ? null : (
      <div
        className="social-pro-pic"
        style={{backgroundImage: `url(${this.props.imageURL})`, margin: '5px', zIndex: '2' }}
      />
    );
    const commentData = (
      <div className="comment-user-data">
        <h4>{ profilePic }</h4>
        <h2>{ this.props.writer }<br/>{parsedDate} at {parsedTime}</h2>
      </div>
    );
    const delBtn = (
        // on button click call to delete comment
        <div className="row-button-comment">
            <button className="row-button" onClick={()=>{

              this.props.deleteComment({msg: this.props.content, writer: this.props.writer, c_id: this.props.c_id});
            }
            }>
                <i className="fa fa-trash-o" />
            </button>
        </div>
    );
    return (<div
      className="comment-slot"
    >
      { commentData }
      { delBtn }
      { commentContent }
    </div>);
  }
}

Comment.defaultProps = {
  content: null,
  writer: null,
  slots: null,
  date: null,
  imageURL: null,
  c_id: null,
};

Comment.propTypes = {
  content: PropTypes.string,
  writer: PropTypes.string,
  date: PropTypes.string,
  imageURL: PropTypes.string,
  deleteComment: PropTypes.func.isRequired,
  c_id: PropTypes.number,
  // schoolSpecificInfo: SemesterlyPropTypes.schoolSpecificInfo.isRequired,
};

export default Comment;
