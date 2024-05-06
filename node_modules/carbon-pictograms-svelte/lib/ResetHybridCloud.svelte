<script>
  /**
   * Specify the pictogram title.
   * @type {string}
   */
  export let title = undefined;

  $: labelled =  $$props["aria-label"] || $$props["aria-labelledby"] || $$props["title"];
  $: attributes = {
    "aria-hidden": labelled ? undefined : true,
    role: labelled ? "img" : undefined,
    focusable: Number($$props["tabindex"]) === 0  ? true : undefined,
  };
</script>

<svg
  preserveAspectRatio="xMidYMid meet"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  width="64"
  height="64"
  fill="currentColor"
  {title}
  {...attributes}
  {...$$restProps}>
  <path d="M25.255,31.255l-0.51-0.51l3.386-3.385H16C8.633,27.36,2.64,21.367,2.64,14	S8.633,0.64,16,0.64S29.36,6.633,29.36,14h-0.72c0-6.97-5.67-12.64-12.64-12.64S3.36,7.03,3.36,14S9.03,26.64,16,26.64h12.131	l-3.386-3.385l0.51-0.51L29.509,27L25.255,31.255z M16,22.36h-0.36v-4.168L12.351,16l6-4l-2.71-1.807V6.368	C11.594,6.557,8.36,9.908,8.36,14c0,3.488,2.356,6.53,5.73,7.399l-0.18,0.697c-3.692-0.951-6.27-4.28-6.27-8.097	c0-4.61,3.75-8.36,8.36-8.36h0.36v4.167L19.649,12l-6,4l2.711,1.808v3.824c4.046-0.188,7.28-3.54,7.28-7.632	c0-3.488-2.355-6.531-5.729-7.399l0.18-0.697c3.691,0.95,6.271,4.28,6.271,8.097C24.36,18.609,20.609,22.36,16,22.36z"></path>
</svg>