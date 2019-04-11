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

import { connect } from 'react-redux';
import AddAdvisorModal from '../../modals/add_advisor_modal';
import { triggerAddAdvisorModal, hideAddAdvisorModal } from '../../../actions/modal_actions';
import { getActiveTimetable } from '../../../reducers/root_reducer';
import { fetchAdvisorLink, fetchAdvisorListLink, fetchAdvisorRemoveLink,  } from '../../../actions/calendar_actions';

const mapStateToProps = (state) => {
  const slots = getActiveTimetable(state).slots;
  return {
    isVisible: state.addAdvisorModal.isVisible,
    data: state.addAdvisorModal.data,
    existingAdvisors: state.addAdvisorModal.existingAdvisors,
    currentTimetableName: state.savingTimetable.activeTimetable.name,
    hasCourses: slots.length > 0,
  };
};

const AddAdvisorModalContainer = connect(
  mapStateToProps,
  {
    triggerAddAdvisorModal,
    hideAddAdvisorModal,
    fetchAdvisorLink,
    fetchAdvisorListLink,
    fetchAdvisorRemoveLink
  },
)(AddAdvisorModal);

export default AddAdvisorModalContainer;
