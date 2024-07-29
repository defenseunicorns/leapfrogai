// Keys returned from the API list call should already be masked for security
// We use this to mask the created key before the user copies it
export const formatKeyShort = (key: string) => {
  const firstTwo = key.slice(0, 5);
  const lastFour = key.slice(-4);
  return `${firstTwo}...${lastFour}`;
};

// Formats a key with several starts in the middle of it based on screen size
// This is used to ensure the "copy key" text input is filled with text regardless of the
// actual key length
export const formatKeyLong = (key: string, width: number) => {
  const approxNumStars = (width) / 4;
  const firstTwo = key.slice(0, 5);
  const lastFour = key.slice(-4);
  return `${firstTwo}${'*'.repeat(approxNumStars)}${lastFour}`;
};
