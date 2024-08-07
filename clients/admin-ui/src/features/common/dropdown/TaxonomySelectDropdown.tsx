import { OptionProps, Options, Select } from "chakra-react-select";
import { Badge, Box, HStack, Text } from "fidesui";

import useTaxonomies from "../hooks/useTaxonomies";

export interface TaxonomySelectOption {
  value: string;
  label: string | JSX.Element;
  description: string;
}

const Option = ({ data, setValue }: OptionProps<TaxonomySelectOption>) => {
  const { getPrimaryKey, getDataCategoryByKey } = useTaxonomies();
  const primaryKey = getPrimaryKey(data.value, 2);
  const primaryCategory = getDataCategoryByKey(primaryKey);

  return (
    <Box
      onClick={() => setValue(data, "select-option")}
      cursor="pointer"
      borderBottomColor="gray.100"
      borderBottomWidth={1}
      paddingX={3}
      paddingY={1.5}
      _hover={{
        backgroundColor: "gray.100",
      }}
      data-testid={`option-${data.value}`}
    >
      <HStack gap={0} alignItems="flex-start">
        <Badge paddingX={1} paddingY={0} bgColor="gray.300" fontSize="xx-small">
          {primaryCategory?.name}
        </Badge>
        <Text fontSize="xs" whiteSpace="normal">
          : {data.description}
        </Text>
      </HStack>
      <Text fontSize="xs" color="gray.500">
        {data.value}
      </Text>
    </Box>
  );
};

interface TaxonomySelectDropdownProps {
  onChange: (selectedOption: TaxonomySelectOption) => void;
  menuIsOpen?: boolean;
  showDisabled?: boolean;
}
const TaxonomySelectDropdown = ({
  onChange,
  menuIsOpen,
  showDisabled = false,
}: TaxonomySelectDropdownProps) => {
  const { getDataCategoryDisplayName, getDataCategories } = useTaxonomies();

  const getActiveDataCategories = () =>
    getDataCategories().filter((c) => c.active);

  const dataCategories = showDisabled
    ? getDataCategories()
    : getActiveDataCategories();

  const options: Options<TaxonomySelectOption> = dataCategories.map(
    (category) => ({
      value: category.fides_key,
      label: getDataCategoryDisplayName(category.fides_key),
      description: category.description || "",
    }),
  );

  return (
    <Select
      placeholder="Select a category"
      onChange={onChange as any}
      options={options}
      size="sm"
      menuPosition="absolute"
      menuPlacement="auto"
      components={{
        Option,
      }}
      menuIsOpen={menuIsOpen}
      chakraStyles={{
        menuList: (baseStyles) => ({
          ...baseStyles,
          paddingTop: 0,
          paddingBottom: 0,
        }),
      }}
    />
  );
};
export default TaxonomySelectDropdown;
