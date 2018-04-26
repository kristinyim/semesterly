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
import Modal from 'boron/WaveModal';

class AddAdvisorModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      input: '',
      advisor: '',
      result: '',
      isLoading: false,
    };
    this.startSearch = this.startSearch.bind(this);
    this.endSearch = this.endSearch.bind(this);
    this.hide = this.hide.bind(this);
  }

  componentWillMount() {
    $(document.body).on('keydown', (e) => {
      if (e.key === 'Enter' && this.state.input.length > 0) {
        this.startSearch();
      }
    });
  }

  componentDidMount() {
    if (this.props.isVisible) {
      this.props.fetchAdvisorListLink();
      this.modal.show();
    }
  }

  componentDidUpdate() {
    if (this.props.isVisible) {
      this.modal.show();
    }
  }

  hide() {
    this.state.result = '';
    this.modal.hide();
  }

  startSearch() {
    this.props.fetchAdvisorLink(this.state.input);
    this.state.isLoading = true;
    this.state.input = '';
    this.state.result = 'One moment...';
  }

  endSearch() {
    this.state.isLoading = false;
    if (!this.props.data.advisors_added) {
      this.state.result = this.props.data.reason || 'Please enter valid email';
    } else if (this.props.data.advisors_added.length > 0) {
      this.state.advisor = this.props.data.advisors_added[0];
      this.state.result = `${this.state.advisor.userFirstName} ${this.state.advisor.userLastName} is now an advisor to your timetable`;
      this.props.fetchAdvisorListLink();
    } else {
      this.state.result = this.props.data.reason === undefined ? 'Please enter valid email' : this.props.data.reason;
    }
  }

  render() {
    const modalHeader =
      (<div className="modal-content">
        <div className="modal-header">
          <div
            className="header-pic add-advisor-header-icon"
          >
            <i className="fa fa-user-plus" />
          </div>
          <h1>Add Advisor</h1>
          <div className="modal-close" onClick={this.hide}>
            <i className="fa fa-times" />
          </div>
        </div>
      </div>);
    const modalStyle = {
      width: '100%',
    };
    if (this.props.data !== '' && this.state.isLoading) {
      this.endSearch();
    }
    const existingAdvisors = this.props.existingAdvisors ? this.props.existingAdvisors.advisors_existing.map((advisor) => (
      <div className="advisor-card" key={advisor}>
        <div
          className="social-pro-pic"
          style={{backgroundImage: `url(${advisor.image_url})`, margin: '5px', zIndex: '2' }}
        />
        <p> {advisor.userFirstName} {advisor.userLastName} - {advisor.email} </p>
      </div>
    )) : null;
    const modalContent = (this.props.hasCourses) ? (
      <div className="add-advisor-modal__container">
        <div className="search-bar__input-wrapper">
          <input
            ref={(c) => { this.input = c; }}
            placeholder={'Search for an Advisor'}
            value={this.state.input}
            className={this.state.isLoading ? 'results-loading-gif' : ''}
            onInput={e => this.setState({ input: e.target.value })}
          />
          <button
            className="btn btn-primary"
            style={{ marginLeft: 'auto', marginRight: '10%' }}
            onClick={() => this.startSearch()}
          >
          Search
        </button>
        <p>{ this.state.result }</p>
          <div className="existing-advisors">
            <h3> Existing Advisors </h3>
            { existingAdvisors }
          </div>
        </div>
      </div>
    ) : (<div className="add-advisor-modal__container">
      <div className="search-bar__input-wrapper">
        <p> Please add to your timetable before adding an advisor </p>
      </div>
    </div>);
    return (
      <Modal
        ref={(c) => { this.modal = c; }}
        className="add-advisor-modal abnb-modal max-modal"
        modalStyle={modalStyle}
        onHide={() => {
          this.props.hideAddAdvisorModal();
          history.replaceState({}, 'Semester.ly', '/');
        }}
      >
        { modalHeader }
        { modalContent }
      </Modal>
    );
  }
}

AddAdvisorModal.propTypes = {
  hideAddAdvisorModal: PropTypes.func.isRequired,
  isVisible: PropTypes.bool.isRequired,
  fetchAdvisorLink: PropTypes.func.isRequired,
  fetchAdvisorListLink: PropTypes.func.isRequired,
};

export default AddAdvisorModal;
