import axiosInstance from '../axios';

export const quizService = {
  // Generate new quiz
  generateQuiz: async (quizData) => {
    try {
      const response = await axiosInstance.post('/quiz/generate', quizData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Submit quiz answers
  submitQuiz: async (quizId, answers, timeTaken = null) => {
    try {
      const response = await axiosInstance.post('/quiz/submit', {
        quiz_id: quizId,
        answers: answers,
        time_taken: timeTaken
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Get quiz history
  getQuizHistory: async (skip = 0, limit = 20) => {
    try {
      const response = await axiosInstance.get('/quiz/history', {
        params: { skip, limit }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Get specific quiz
  getQuiz: async (quizId) => {
    try {
      const response = await axiosInstance.get(`/quiz/${quizId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Get quiz statistics
  getQuizStats: async () => {
    try {
      const history = await quizService.getQuizHistory(0, 100);
      const completed = history.filter(q => q.is_completed);
      const totalScore = completed.reduce((sum, q) => sum + (q.percentage || 0), 0);
      const avgScore = completed.length > 0 ? totalScore / completed.length : 0;

      return {
        total: history.length,
        completed: completed.length,
        averageScore: avgScore,
        passed: completed.filter(q => (q.percentage || 0) >= 60).length
      };
    } catch (error) {
      throw error.response?.data || error;
    }
  }
};