export const cn = (...classes) => {
  return classes.filter(Boolean).join(' ');
};

export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

export const handleApiError = (error) => {
  if (error.response) {
    const status = error.response.status;
    const message = error.response.data?.detail || 'An error occurred';
    
    switch (status) {
      case 400:
        return message;
      case 401:
        return 'Please login again';
      case 403:
        return "You don't have permission";
      case 404:
        return 'Resource not found';
      case 422:
        return typeof message === 'string' ? message : 'Validation error';
      case 500:
        return 'Server error. Please try again later';
      default:
        return message;
    }
  } else if (error.request) {
    return 'Cannot connect to server. Please check your internet connection';
  } else {
    return error.message || 'An unexpected error occurred';
  }
};

export const formatPercentage = (value) => {
  return `${value.toFixed(1)}%`;
};

export const getScoreColor = (percentage) => {
  if (percentage >= 80) return 'text-green-600';
  if (percentage >= 60) return 'text-blue-600';
  if (percentage >= 40) return 'text-yellow-600';
  return 'text-red-600';
};
