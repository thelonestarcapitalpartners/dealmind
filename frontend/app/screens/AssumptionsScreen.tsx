import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, TextInput, Button } from 'react-native-paper';

/**
 * Assumptions Screen - Edit deal assumptions and parameters
 * 
 * Editable fields:
 * - Purchase price
 * - Rent (monthly/annual)
 * - Vacancy rate
 * - Operating expenses
 * - Financing terms
 * - Exit assumptions
 */
export default function AssumptionsScreen({ navigation, route }) {
  const { dealId } = route.params;
  const [assumptions, setAssumptions] = React.useState({
    purchasePrice: '500000',
    monthlyRent: '2500',
    vacancyRate: '5',
    propertyTaxes: '3000',
    insurance: '1200',
    repairs: '2000',
    downPayment: '25',
    interestRate: '6.5',
    loanTerm: '30',
  });

  const handleAssumptionChange = (key, value) => {
    setAssumptions(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    // TODO: Save assumptions to API
    navigation.goBack();
  };

  return (
    <ScrollView style={styles.container}>
      <Text variant="headlineSmall" style={styles.section}>
        Property Details
      </Text>
      <TextInput
        label="Purchase Price"
        value={assumptions.purchasePrice}
        onChangeText={(v) => handleAssumptionChange('purchasePrice', v)}
        keyboardType="decimal-pad"
        style={styles.input}
      />
      <TextInput
        label="Monthly Rent"
        value={assumptions.monthlyRent}
        onChangeText={(v) => handleAssumptionChange('monthlyRent', v)}
        keyboardType="decimal-pad"
        style={styles.input}
      />

      <Text variant="headlineSmall" style={styles.section}>
        Operating Expenses
      </Text>
      <TextInput
        label="Vacancy Rate (%)"
        value={assumptions.vacancyRate}
        onChangeText={(v) => handleAssumptionChange('vacancyRate', v)}
        keyboardType="decimal-pad"
        style={styles.input}
      />
      <TextInput
        label="Annual Property Taxes"
        value={assumptions.propertyTaxes}
        onChangeText={(v) => handleAssumptionChange('propertyTaxes', v)}
        keyboardType="decimal-pad"
        style={styles.input}
      />
      <TextInput
        label="Annual Insurance"
        value={assumptions.insurance}
        onChangeText={(v) => handleAssumptionChange('insurance', v)}
        keyboardType="decimal-pad"
        style={styles.input}
      />
      <TextInput
        label="Annual Repairs & Maintenance"
        value={assumptions.repairs}
        onChangeText={(v) => handleAssumptionChange('repairs', v)}
        keyboardType="decimal-pad"
        style={styles.input}
      />

      <Text variant="headlineSmall" style={styles.section}>
        Financing
      </Text>
      <TextInput
        label="Down Payment (%)"
        value={assumptions.downPayment}
        onChangeText={(v) => handleAssumptionChange('downPayment', v)}
        keyboardType="decimal-pad"
        style={styles.input}
      />
      <TextInput
        label="Interest Rate (%)"
        value={assumptions.interestRate}
        onChangeText={(v) => handleAssumptionChange('interestRate', v)}
        keyboardType="decimal-pad"
        style={styles.input}
      />
      <TextInput
        label="Loan Term (Years)"
        value={assumptions.loanTerm}
        onChangeText={(v) => handleAssumptionChange('loanTerm', v)}
        keyboardType="decimal-pad"
        style={styles.input}
      />

      <Button
        mode="contained"
        onPress={handleSave}
        style={styles.saveButton}
      >
        Save & Recalculate
      </Button>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  section: {
    marginTop: 20,
    marginBottom: 12,
    fontWeight: '600',
  },
  input: {
    marginBottom: 12,
  },
  saveButton: {
    marginTop: 24,
    marginBottom: 32,
    paddingVertical: 6,
  },
});
