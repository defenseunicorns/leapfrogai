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
  <path d="M31,31.36H1v-0.72h30V31.36z M31,28.36H1v-0.72h30V28.36z M31,25.36H1v-0.72h30V25.36z M31,22.36H1c-0.199,0-0.36-0.161-0.36-0.36V1c0-0.199,0.161-0.36,0.36-0.36h30c0.199,0,0.36,0.161,0.36,0.36v21	C31.36,22.199,31.199,22.36,31,22.36z M1.36,21.64h29.28V4.36H1.36V21.64z M1.36,3.64h29.28V1.36H1.36V3.64z M29,2.5	C29,2.776,28.776,3,28.5,3S28,2.776,28,2.5S28.224,2,28.5,2S29,2.224,29,2.5z M26.5,2C26.224,2,26,2.224,26,2.5S26.224,3,26.5,3	S27,2.776,27,2.5S26.776,2,26.5,2z M24.5,2C24.224,2,24,2.224,24,2.5S24.224,3,24.5,3S25,2.776,25,2.5S24.776,2,24.5,2z M10,14.36H4	v-0.72h6V14.36z M10,11.36H4v-0.72h6V11.36z M10,8.36H4V7.64h6V8.36z"></path>
</svg>