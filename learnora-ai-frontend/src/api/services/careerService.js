import axiosInstance from '../axios';

export const careerService = {
  // Submit career assessment
  assessCareer: async (assessmentData) => {
    try {
      const response = await axiosInstance.post('/career/assess', assessmentData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Get career profile
  getCareerProfile: async () => {
    try {
      const response = await axiosInstance.get('/career/profile');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Get assessment history
  getAssessmentHistory: async () => {
    try {
      const response = await axiosInstance.get('/career/history');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  }
};