import axiosInstance from '../axios';

export const doubtService = {
  // Ask a doubt
  askDoubt: async (doubtData) => {
    try {
      const response = await axiosInstance.post('/doubts/ask', doubtData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Ask doubt with file
  askDoubtWithFile: async (question, subject, file) => {
    try {
      const formData = new FormData();
      formData.append('question', question);
      if (subject) formData.append('subject', subject);
      formData.append('file', file);

      const response = await axiosInstance.post('/doubts/ask-with-file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Ask follow-up question
  askFollowUp: async (doubtId, question) => {
    try {
      const response = await axiosInstance.post('/doubts/follow-up', {
        doubt_id: doubtId,
        question: question
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Rate doubt solution
  rateDoubt: async (doubtId, rating, feedback = null) => {
    try {
      const response = await axiosInstance.post('/doubts/rate', {
        doubt_id: doubtId,
        rating: rating,
        feedback: feedback
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Get doubt history
  getDoubtHistory: async (skip = 0, limit = 20) => {
    try {
      const response = await axiosInstance.get('/doubts/history', {
        params: { skip, limit }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Get specific doubt
  getDoubt: async (doubtId) => {
    try {
      const response = await axiosInstance.get(`/doubts/${doubtId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  }
};