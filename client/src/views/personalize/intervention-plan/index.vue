<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { useInterventionPlan } from "./utils/hook";
import { ref } from "vue";

defineOptions({
  name: "InterventionPlan"
});

const tableRef = ref();
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat
} = useInterventionPlan(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="interventionPlan"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
  />
</template>
