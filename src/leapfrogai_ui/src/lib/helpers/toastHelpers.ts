import {
  BanOutline,
  CheckCircleSolid,
  ExclamationCircleOutline,
  InfoCircleOutline
} from 'flowbite-svelte-icons';

export const getColor = (toastKind: ToastKind) => {
  switch (toastKind) {
    case 'success':
      return 'green';
    case 'info':
      return 'blue';
    case 'warning':
      return 'yellow';
    case 'error':
      return 'red';
    default:
      return 'blue';
  }
};

export const getIconComponent = (toastKind: ToastKind) => {
  switch (toastKind) {
    case 'success':
      return CheckCircleSolid;
    case 'info':
      return InfoCircleOutline;
    case 'warning':
      return ExclamationCircleOutline;
    case 'error':
      return BanOutline;
    default:
      return InfoCircleOutline;
  }
};
