type ToastStore = {
	toasts: ToastNotificationProps[];
};

type RequiredToastFields = Pick<ToastNotificationProps, 'title' | 'subtitle'>;
type OptionalToastFields = Partial<Omit<ToastNotificationProps, 'title' | 'subtitle'>>;
