type ToastErrorText = {
  title: string;
  subtitle?: string;
};

export const ERROR_SAVING_MSG_TEXT: ToastErrorText = {
  title: 'Error',
  subtitle: 'Error saving message. Please try again.'
};

export const ERROR_GETTING_AI_RESPONSE_TEXT: ToastErrorText = {
  title: 'Error',
  subtitle: 'Error getting AI Response'
};

export const ERROR_GETTING_ASSISTANT_MSG_TEXT: ToastErrorText = {
  title: 'Error',
  subtitle: 'Error getting Assistant Response'
};
