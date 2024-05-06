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
  <path d="M31,18.559v-0.985L17.36,4.844V2c0-0.096-0.038-0.187-0.105-0.254l-1-1	c-0.141-0.141-0.368-0.141-0.509,0l-1,1C14.678,1.813,14.64,1.904,14.64,2v2.844L1,17.574v0.985L14.64,5.828v2.015L1,20.574v0.985	L14.64,8.828v2.015L1,23.574v0.985l13.64-12.731v2.015L1,26.574v0.985L13.406,15.98L5.295,29.64H1v0.721h30V29.64h-4.295	l-8.109-13.658L31,27.559v-0.985l-13.64-12.73v-2.015L31,24.559v-0.985l-13.64-12.73V8.829L31,21.559v-0.985L17.36,7.844V5.829	L31,18.559z M8.621,29.64L16,16.726l7.379,12.914H8.621z M25.867,29.64h-1.659l-7.896-13.818c-0.128-0.225-0.497-0.225-0.625,0	L7.791,29.64H6.133l9.177-15.456c0.033-0.056,0.05-0.119,0.05-0.184V2.149L16,1.509l0.64,0.64V14c0,0.064,0.017,0.128,0.05,0.184	L25.867,29.64z"></path>
</svg>