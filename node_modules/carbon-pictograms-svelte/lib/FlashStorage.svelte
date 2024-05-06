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
  <path d="M31,27.36H1c-0.199,0-0.36-0.161-0.36-0.36v-9c0-0.199,0.161-0.36,0.36-0.36h17v0.721H1.36v8.279	h29.28v-8.28H24v-0.72h7c0.199,0,0.36,0.161,0.36,0.36v9C31.36,27.199,31.199,27.36,31,27.36z M17.309,25.186l-0.617-0.371	l5.673-9.455H17c-0.127,0-0.245-0.067-0.31-0.176c-0.065-0.109-0.067-0.245-0.006-0.356l6-11l0.633,0.345l-5.71,10.468H23	c0.13,0,0.249,0.07,0.313,0.183c0.063,0.113,0.062,0.251-0.005,0.362L17.309,25.186z M10.36,24H9.64v-3h0.72	C10.36,21,10.36,24,10.36,24z M8.36,24H7.64v-3h0.72V24z M6.36,24H5.64v-3h0.72C6.36,21,6.36,24,6.36,24z M4.36,24H3.64v-3h0.72V24z M31,15.36h-6v-0.72h5.64V6.36H25V5.64h6c0.199,0,0.36,0.161,0.36,0.36v9C31.36,15.199,31.199,15.36,31,15.36z M15,15.36H1	c-0.199,0-0.36-0.161-0.36-0.36V6c0-0.199,0.161-0.36,0.36-0.36h18v0.72H1.36v8.28H15V15.36z M10.36,12H9.64V9h0.72	C10.36,9,10.36,12,10.36,12z M8.36,12H7.64V9h0.72V12z M6.36,12H5.64V9h0.72C6.36,9,6.36,12,6.36,12z M4.36,12H3.64V9h0.72V12z"></path>
</svg>