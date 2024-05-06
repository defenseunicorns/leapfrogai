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
  <path d="M29,3.5C29,3.776,28.776,4,28.5,4S28,3.776,28,3.5S28.224,3,28.5,3S29,3.224,29,3.5z M26.5,3	C26.224,3,26,3.224,26,3.5S26.224,4,26.5,4S27,3.776,27,3.5S26.776,3,26.5,3z M24.5,3C24.224,3,24,3.224,24,3.5S24.224,4,24.5,4	S25,3.776,25,3.5S24.776,3,24.5,3z M31,30.36H1c-0.199,0-0.36-0.161-0.36-0.36V2c0-0.199,0.161-0.36,0.36-0.36h30	c0.199,0,0.36,0.161,0.36,0.36v28C31.36,30.199,31.199,30.36,31,30.36z M9.36,29.64h21.28V5.36H9.36V29.64z M1.36,29.64h7.28V5.36	H1.36V29.64z M9,4.64h21.64V2.36H1.36v2.28H9z"></path>
</svg>