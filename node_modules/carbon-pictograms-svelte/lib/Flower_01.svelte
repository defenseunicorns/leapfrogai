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
  <path d="M31,31.36H1v-0.72h14.64v-9.371c-6.919-2.125-7-8.207-7-8.269c0-0.199,0.161-0.36,0.36-0.36	c0.059,0,4.799,0.062,6.64,4.406v-5.698c-2.789-0.186-5-2.514-5-5.348V1c0-0.199,0.161-0.36,0.36-0.36	c0.043,0,2.935,0.033,4.803,1.997C16.188,2.091,17.538,0.64,21,0.64c0.199,0,0.36,0.161,0.36,0.36v5c0,2.834-2.212,5.162-5,5.348	v10.698c1.841-4.344,6.581-4.406,6.64-4.406c0.199,0,0.36,0.161,0.36,0.36c0,0.212-0.081,5.169-7,8.235v4.404H31V31.36z M22.608,18.382c-1.396,0.13-5.97,1.017-6.236,7.058C21.562,23.022,22.455,19.539,22.608,18.382z M9.383,13.381	c0.127,1.284,0.951,5.4,6.248,7.129C15.396,14.394,10.774,13.509,9.383,13.381z M11.36,1.378V6c0,2.559,2.082,4.64,4.64,4.64	S20.64,8.559,20.64,6V1.366c-3.396,0.108-4.282,1.727-4.319,1.798l-0.124-0.063C16.886,4.018,17.36,5.275,17.36,7h-0.72	C16.64,2.202,12.614,1.485,11.36,1.378z"></path>
</svg>