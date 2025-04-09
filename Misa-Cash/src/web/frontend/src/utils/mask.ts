// Aplica uma máscara a um valor
export const applyMask = (value: string, mask: string): string => {
  let result = '';
  let valueIndex = 0;
  let maskIndex = 0;

  while (valueIndex < value.length && maskIndex < mask.length) {
    const maskChar = mask[maskIndex];
    const valueChar = value[valueIndex];

    if (maskChar === '#') {
      if (/\d/.test(valueChar)) {
        result += valueChar;
        valueIndex++;
      }
    } else if (maskChar === '@') {
      if (/[a-zA-Z]/.test(valueChar)) {
        result += valueChar;
        valueIndex++;
      }
    } else if (maskChar === '*') {
      if (/[a-zA-Z0-9]/.test(valueChar)) {
        result += valueChar;
        valueIndex++;
      }
    } else {
      result += maskChar;
    }

    maskIndex++;
  }

  return result;
};

// Remove uma máscara de um valor
export const removeMask = (value: string, mask: string): string => {
  let result = '';
  let valueIndex = 0;
  let maskIndex = 0;

  while (valueIndex < value.length && maskIndex < mask.length) {
    const maskChar = mask[maskIndex];
    const valueChar = value[valueIndex];

    if (maskChar === '#' || maskChar === '@' || maskChar === '*') {
      result += valueChar;
      valueIndex++;
    } else if (maskChar === valueChar) {
      valueIndex++;
    }

    maskIndex++;
  }

  return result;
};

// Máscaras comuns
export const masks = {
  // CPF: xxx.xxx.xxx-xx
  cpf: '###.###.###-##',

  // CNPJ: xx.xxx.xxx/xxxx-xx
  cnpj: '##.###.###/####-##',

  // Telefone: (xx) xxxxx-xxxx
  phone: '(##) #####-####',

  // Telefone: (xx) xxxx-xxxx
  phone8: '(##) ####-####',

  // CEP: xxxxx-xxx
  cep: '#####-###',

  // Data: dd/mm/yyyy
  date: '##/##/####',

  // Hora: HH:mm
  time: '##:##',

  // Data e Hora: dd/mm/yyyy HH:mm
  dateTime: '##/##/#### ##:##',

  // Cartão de Crédito: xxxx xxxx xxxx xxxx
  creditCard: '#### #### #### ####',

  // Cartão de Crédito (mascarado): xxxx xxxx xxxx ****
  creditCardMasked: '#### #### #### ****',

  // Moeda: R$ #.###,00
  currency: 'R$ #.###,00',

  // Percentual: #,##%
  percentage: '#,##%',

  // Número: #.###,00
  number: '#.###,00',

  // Número Inteiro: #.###
  integer: '#.###',

  // Email: xxxxx@xxxxx.xxx
  email: '@@@@@@@@@@@.@@@',

  // URL: http://xxxxx.xxx
  url: 'http://@@@@@@@.@@@',

  // IP: xxx.xxx.xxx.xxx
  ip: '###.###.###.###',

  // MAC: xx:xx:xx:xx:xx:xx
  mac: '##:##:##:##:##:##',

  // RG: xx.xxx.xxx-x
  rg: '##.###.###-#',

  // Título Eleitoral: xxxxx.xxx.xxx.xxx
  voterId: '#####.###.###.###',

  // PIS/PASEP: xxx.xxxxx.xxx-x
  pis: '###.#####.###-#',

  // CNS: xxx xxxx xxxx xxxx
  cns: '### #### #### ####',
};

// Aplica uma máscara pré-definida
export const applyPredefinedMask = (value: string, maskType: keyof typeof masks): string => {
  return applyMask(value, masks[maskType]);
};

// Remove uma máscara pré-definida
export const removePredefinedMask = (value: string, maskType: keyof typeof masks): string => {
  return removeMask(value, masks[maskType]);
};

// Verifica se um valor está de acordo com uma máscara
export const isValidMaskedValue = (value: string, mask: string): boolean => {
  const cleanValue = removeMask(value, mask);
  const expectedLength = mask.replace(/[^#@*]/g, '').length;
  return cleanValue.length === expectedLength;
};

// Obtém o próximo caractere da máscara
export const getNextMaskChar = (value: string, mask: string): string => {
  const currentLength = removeMask(value, mask).length;
  let maskIndex = 0;
  let valueIndex = 0;

  while (valueIndex < currentLength && maskIndex < mask.length) {
    const maskChar = mask[maskIndex];
    if (maskChar === '#' || maskChar === '@' || maskChar === '*') {
      valueIndex++;
    }
    maskIndex++;
  }

  return mask[maskIndex] || '';
}; 