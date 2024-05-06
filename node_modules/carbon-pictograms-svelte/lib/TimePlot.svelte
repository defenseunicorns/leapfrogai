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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V1h0.72v14.64H11c0.096,0,0.187,0.038,0.254,0.105	l7.895,7.894H31v0.721H19c-0.096,0-0.188-0.038-0.255-0.105l-7.894-7.895H1.36v14.28H31V31.36z M24,15.36	c-4.059,0-7.36-3.302-7.36-7.36S19.941,0.64,24,0.64S31.36,3.942,31.36,8S28.059,15.36,24,15.36z M17.37,8.36	c0.181,3.376,2.895,6.089,6.27,6.271V13h0.721v1.63c3.375-0.181,6.089-2.895,6.27-6.271H29V7.64h1.63	c-0.181-3.376-2.895-6.089-6.27-6.271V3h-0.72V1.37c-3.375,0.181-6.089,2.895-6.27,6.271H19v0.72h-1.63V8.36z M25.745,10.254l-2-2	C23.678,8.187,23.64,8.096,23.64,8V4h0.721v3.851l1.895,1.895L25.745,10.254z"></path>
</svg>